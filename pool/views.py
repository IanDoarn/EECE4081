from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Game, Bet
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from pool.models import Season

def endOfSeasonalWeek(dt):
    dtnm = stripMicroseconds(dt)
    season = Season.objects.get(start__lte=dtnm, end__gte=dtnm)
    i = startOfSeasonalWeek(dt) + timedelta(days=6)
    if  i > season.end:
        i = season.end
    return datetime(i.year, i.month, i.day, 23, 59, 59, 999999, i.tzinfo)

def lastWeek(dt):
    return stripTime(dt) - timedelta(days=7)

def mondayOfSameWeek(dt):
    i =    stripTime(dt)
    j =      i.weekday()
    return i - timedelta(days=j)

def nextWeek(dt):
    return stripTime(dt) + timedelta(days=7)

def stripMicroseconds(dt):
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=dt.tzinfo)

def stripTime(dt):
    return datetime(dt.year, dt.month, dt.day, tzinfo=dt.tzinfo)

def seasonalWeek(dt):
    dtnm = stripMicroseconds(dt)
    season = Season.objects.get(start__lte=dtnm, end__gte=dtnm)
    i = startOfSeasonalWeek(dt)
    j = 1
    while i > season.start:
        i = i - timedelta(days=7)
        j = j + 1
    return j

def startOfSeasonalWeek(dt):
    dtmn = stripMicroseconds(dt)
    season = Season.objects.get(start__lte=dtmn, end__gte=dtmn)
    i = stripTime(dt)
    if i.weekday() >= season.start.weekday():
        i = i - timedelta(days=(i.weekday()-   season.start.weekday() ))
    else:
        i = i - timedelta(days=i.weekday())
        i = i - timedelta(days=7)
        i = i + timedelta(days=season.start.weekday())
    if  i < season.start:
        i = season.start
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
    
    week = None
    dt = timezone.now()
    try:
        week = seasonalWeek(dt)
    except ObjectDoesNotExist:
        pass

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
    
    ### GET SEASON ###
    
    try:
        season = Season.objects.get(start__lte=dt, end__gte=dt)
    except ObjectDoesNotExist:
        season = None

    # Clearly need to work on this.


    # OLD CODE BELOW


    try:
        if season == None:
            raise ObjectDoesNotExist()
        games = Game.objects.filter(date_time__range=(
            season.start, endOfSeasonalWeek(lastWeek(dt))
                # todo: replace with start and end of season
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

    #################
    # RENDER OUTPUT #
    #################
    
    return render(
        request, 'home.html',
        {
            'title': "Winston Cup Week " + str(week) if week != None else "Out of season",
            'games': Game.objects.filter(date_time__range=(
                        lastWeek(timezone.now()),
                        nextWeek(timezone.now())
                     )).order_by('date_time'),
            'table_headers': ['Favorite', 'Line', 'Underdog', 'TV', 'Date / Time'],
            'first': first, 'second': second
        }
    )


@login_required
def profile(request):
    # TODO: Watch video and implement functionality to retrieve bets from Bet table
    # https://www.youtube.com/watch?v=VxOsCKMStuw&index=48&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj

    return render(request, 'accounts/profile.html')


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