from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Game, Bet
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from pool.models import Season

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

def sundayOfSameWeek(dt):
    i =    stripTime(dt)
    j =  6 - i.weekday()
    k =  i + timedelta(days=j)
    return datetime(k.year, k.month, k.day, 23, 59, 59, 999999, k.tzinfo)

def endOfSeasonalWeek(dt):
    season = Season.objects.get(start__gte=dt, end__lte=dt)
    i = startOfSeasonalWeek(dt) + timedelta(days=6)
    if  i > season.end:
        i = season.end
    return datetime(i.year, i.month, i.day, 23, 59, 59, 999999, i.tzinfo)

def seasonalWeek(dt):
    season = Season.objects.get(start__gte=dt, end__lte=dt)
    i = startOfSeasonalWeek(dt)
    j = 1
    while i > season.start:
        i = i - timedelta(days=7)
        j = j + 1
    return j

def startOfSeasonalWeek(dt):
    season = Season.objects.get(start__gte=dt, end__lte=dt)
    i = stripTime(dt)
    i = i - timedelta(days=7-season.start.weekday()) - timedelta(days=i.weekday())
    if  i < season.start:
        i = season.start
    return i

@login_required
def home(request):

    # TESTING ONLY    
    try:
        dt = timezone.now()
        while True:
            print(str(dt) + ", " + str(startOfSeasonalWeek(dt)) + ", " + str(endOfSeasonalWeek(dt)) + ", " + str(seasonalWeek(dt)))
            dt = dt + timedelta(days=1)
    except ObjectDoesNotExist:
        pass
    # END OF TESTING ONLY

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
    game_ids  = []
    for game in games:
        game_ids.append(game.id)            
    try:
        bets = Bet.objects.filter(game_id__in=game_ids)
    except ObjectDoesNotExist:
        bets = []
    points = {}
    for bet in bets:
        try:
            value = points[bet.user]
        except KeyError:
            value = 0
        if bet.game_id.underdog_score != None and bet.game_id.favorite_score != None:
            if bet.team_id == bet.game_id.underdog_id:
                if bet.game_id.favorite_score < (bet.game_id.underdog_score + bet.game_id.spread):
                    won = True
                else:
                    won = False
            else:
                if bet.game_id.underdog_score < (bet.game_id.favorite_score - bet.game_id.spread):
                    won = True
                else:
                    won = False
            if won:
                value = value + 1
                if bet.game_id.is_game_of_week:
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
                        
    print(str(first))
    print(str(second))
                        
    ##########################
    # WINSTON CUP SCOREBOARD #
    ##########################
    
    ### GET SEASON ###
    
    try:
        season = Season.objects.get(start__gte=dt, end__lte=dt)
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
    game_ids  = []
    for game in games:
        game_ids.append(game.id)
    try:
        bets = Bet.objects.filter(game_id__in=game_ids)
    except ObjectDoesNotExist:
        bets = []    
    points = {}
    for bet in bets:
        try:
            value = points[bet.user]
        except KeyError:
            value = 0
        if bet.game_id.underdog_score != None and bet.game_id.favorite_score != None:
            if bet.team_id == bet.game_id.underdog_id:
                if bet.game_id.favorite_score < (bet.game_id.underdog_score + bet.game_id.spread):
                    won = True
                else:
                    won = False
            else:
                if bet.game_id.underdog_score < (bet.game_id.favorite_score - bet.game_id.spread):
                    won = True
                else:
                    won = False
            if won:
                value = value + 1
                if bet.is_high_risk:
                    value = value + 5
                if bet.game_id.is_game_of_week:
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
             'first': first, #,
            'second': second# None if second == None else second.name
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