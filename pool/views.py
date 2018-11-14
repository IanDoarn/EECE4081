from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Game, Bet
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from pool.models import Season, Subscription, SeasonalSubscription
from django_tables2 import RequestConfig
from .tables import GameTable
from .forms import BetForm
from django.contrib import messages


def endOfSeasonalWeek(dt, season):
    if  season == None:
        try:
            season = Season.objects.get(start__lte=dt, end__gte=dt)
        except ObjectDoesNotExist:
            return None
    if dt.date() > season.end:
        return None
    i = startOfSeasonalWeek(dt, season) + timedelta(days=6)
    if  i.date() > season.end:
        i = datetime(season.end.year, season.end.month, season.end.day,              tzinfo=i.tzinfo)
    return  datetime(         i.year,          i.month,          i.day, 23, 59, 59, 999999, i.tzinfo)

def lastWeek(dt):
    return stripTime(dt) - timedelta(days=7)

def mondayOfSameWeek(dt):
    i =    stripTime(dt)
    j =      i.weekday()
    return i - timedelta(days=j)

def nextWeek(dt):
    return stripTime(dt) + timedelta(days=7)

def stripTime(dt):
    return datetime(dt.year, dt.month, dt.day, tzinfo=dt.tzinfo)

def seasonalWeek(dt, season):
    if  season == None:
        try:
            season = Season.objects.get(start__lte=dt, end__gte=dt)
        except ObjectDoesNotExist:
            return None
    if dt.date() > season.end:
        return None
    i = startOfSeasonalWeek(dt, season)
    j = 1
    while i.date() > season.start:
        i = i - timedelta(days=7)
        j = j + 1
    return j

def startOfSeasonalWeek(dt, season):
    if  season == None:
        try:
            season = Season.objects.get(start__lte=dt, end__gte=dt)
        except ObjectDoesNotExist:
            return None
    if dt.date() > season.end:
        return None    
    i = stripTime(dt)
    if i.weekday() >= season.start.weekday():
        i = i - timedelta(days=(i.weekday()-season.start.weekday()))
    else:
        i = i - timedelta(days=i.weekday())
        i = i - timedelta(days=7)
        i = i + timedelta(days=season.start.weekday())
    if  i.date() < season.start:
        i = datetime(season.start.year, season.start.month, season.start.day, tzinfo=i.tzinfo)
    return i

def sundayOfSameWeek(dt):
    i =    stripTime(dt)
    j =  6 - i.weekday()
    k =  i + timedelta(days=j)
    return datetime(k.year, k.month, k.day, 23, 59, 59, 999999, k.tzinfo)

@login_required
def home(request):

    #################
    # MISCELLANEOUS #
    #################
    
    dt = timezone.now()

    ##################
    # WEEKLY SCORING #
    ##################

    try:
        games = Game.objects.filter(date_time__range=(
            mondayOfSameWeek(lastWeek(dt)),
            sundayOfSameWeek(lastWeek(dt))
        ))
    except ObjectDoesNotExist:
        games = []
    try:
        bets = Bet.objects.filter(game__in=games)
    except ObjectDoesNotExist:
        bets = []
    points = {}
    for bet in bets:
        try:
            value = points[bet.user]
        except KeyError:
            value = 0
        if bet.game.underdog_score != None and bet.game.favorite_score != None:
            if bet.team == bet.game.underdog:
                if bet.game.favorite_score < (bet.game.underdog_score + bet.game.spread):
                    won = True
                else:
                    won = False
            else:
                if bet.game.underdog_score < (bet.game.favorite_score - bet.game.spread):
                    won = True
                else:
                    won = False
            if won:
                value = value + 1
                if bet.game.is_game_of_week:
                    value = value + 2             
        points[bet.user] = value
    first  = None
    second = None    
    for user in points:
        if  first == None:
            if points[user] > 0:
                first  =  user
        else:
            if points[user] >= points[first]:
                second = first
                first  =  user
            else:
                if  second == None:
                    if points[user] > 0:
                        second = user
                else:
                    if points[user] >= points[second]:
                        second = user
                        
    ##########################
    # WINSTON CUP SCOREBOARD #
    ##########################
    
    try:
        season     = Season.objects.get(start__lte=dt, end__gte=dt)
    except ObjectDoesNotExist:
        try:
            season = Season.objects.filter(end__lte=dt).order_by('end').last()
        except ObjectDoesNotExist:
            season = None

    if season != None:
        end = endOfSeasonalWeek(lastWeek(dt), season)
        if  end == None:
            end = datetime(season.end.year, season.end.month, season.end.day, tzinfo=dt.tzinfo)

    try:
        if season == None:
            raise ObjectDoesNotExist()
        games = Game.objects.filter(date_time__range=(
            datetime(season.start.year, season.start.month, season.start.day, tzinfo=dt.tzinfo), end
        ))
    except ObjectDoesNotExist:
        games = []
    try:
        bets = Bet.objects.filter(game__in=games)
    except ObjectDoesNotExist:
        bets = []    
    points = {}
    for bet in bets:
        try:
            value = points[bet.user]
        except KeyError:
            value = 0
        if bet.game.underdog_score != None and bet.game.favorite_score != None:
            if bet.team == bet.game.underdog:
                if bet.game.favorite_score < (bet.game.underdog_score + bet.game.spread):
                    won = True
                else:
                    won = False
            else:
                if bet.game.underdog_score < (bet.game.favorite_score - bet.game.spread):
                    won = True
                else:
                    won = False
            if won:
                value = value + 1
                if bet.is_high_risk:
                    value = value + 5
                if bet.game.is_game_of_week:
                    value = value + 2
            else:
                if bet.is_high_risk:
                    value = value - 5             
        points[bet.user] = value
    try:
        if season == None:
            raise ObjectDoesNotExist()
        games = games.filter(date_time__range=(startOfSeasonalWeek(lastWeek(dt), season), end))
    except ObjectDoesNotExist:
        games = []
    try:
        bets = Bet.objects.filter(game__in=games)
    except ObjectDoesNotExist:
        bets = []    
    change = {}
    for bet in bets:
        try:
            value = change[bet.user]
        except KeyError:
            value = 0
        if bet.game.underdog_score != None and bet.game.favorite_score != None:
            if bet.team == bet.game.underdog:
                if bet.game.favorite_score < (bet.game.underdog_score + bet.game.spread):
                    won = True
                else:
                    won = False
            else:
                if bet.game.underdog_score < (bet.game.favorite_score - bet.game.spread):
                    won = True
                else:
                    won = False
            if won:
                value = value + 1
                if bet.is_high_risk:
                    value = value + 5
                if bet.game.is_game_of_week:
                    value = value + 2
            else:
                if bet.is_high_risk:                  
                    value = value - 5             
        change[bet.user] = value

    if season != None:
        try:
            value = points[request.user]
        except KeyError:
            points[request.user]     = 0
            if len(change)          != 0:
                change[request.user] = 0


    # TESTING ONLY
    print("From WC Points:")        
    for user in points:
        print(str(user) + ": " + str(points[user]))
    
    print("From WC Change:")
    for user in change:
        print(str(user) + ": " + str(change[user]))
    # TESTING ONLY
        
    # todo: figure out how to organize and convey points/change
    
    last_week = seasonalWeek(lastWeek(dt), season)
    this_week = seasonalWeek(         dt , season)
    
    print(str(last_week))
    print(str(this_week))

    #################
    # RENDER OUTPUT #
    #################

    
    return render(
        request, 'home.html',
        {
            'title': ("Winston Cup Week " + str(this_week)) if this_week != None else "Out of season",
            'games': Game.objects.filter(date_time__range=(lastWeek(dt), nextWeek(dt))).order_by('date_time'),
            'table_headers': ['Favorite', 'Line', 'Underdog', 'TV', 'Date / Time'],
            'first': first, 'second': second,
            'week_header': "Week " + str(last_week) if last_week != None else ""
        }
    )


@login_required
def profile(request):
    return render(
        request, 'accounts/profile.html',
        {
            'bets': Bet.objects.filter(user=request.user).order_by('date_time')
        }
    )

def games(request):
    table = GameTable(Game.objects.all())
    RequestConfig(request).configure(table)

    if request.POST:
        # this is a terrible fucking way to do this but we literally
        # do not have time to figure the right way out
        request.session['current_bet_id'] = list(dict(request.POST))[1]
        return redirect('betpage')

    return render(request, 'games.html', {'table': table})

@login_required
def betpage(request):
    # Set session tokens to determine if use has a subscription
    # and / or user has registered for the current season

    subscription = Subscription.objects.filter(user=request.user).first()
    season_subscription = SeasonalSubscription.objects.filter(user=request.user).first()

    betform = BetForm()

    print(subscription)
    print(season_subscription)

    if request.POST:
        betform = BetForm(request.POST)
        if betform.is_valid():
            del request.session['current_bet_id']
            return redirect('games')
        else:
            del request.session['current_bet_id']
            pass

    return render(request, 'betpage.html',
                  {'form': betform,
                   'game': Game.objects.filter(id=request.session['current_bet_id'].split('_')[2]).first(),
                   'subscription': subscription,
                   'seasonal_subscription': season_subscription
                   }
                  )

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})