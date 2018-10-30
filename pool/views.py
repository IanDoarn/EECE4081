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
    season = Season.objects.get(start__lte=dt, end__gte=dt)
    i = startOfSeasonalWeek(dt) + timedelta(days=6)
    if  i > season.end:
        i = season.end
    return datetime(i.year, i.month, i.day, 23, 59, 59, 999999, i.tzinfo)

def seasonalWeek(dt):
    season = Season.objects.get(start__lte=dt, end__gte=dt)
    i = startOfSeasonalWeek(dt)
    j = 1
    while i > season.start:
        i = i - timedelta(days=7)
        j = j + 1
    return j

def startOfSeasonalWeek(dt):
    # This function has a bug.
    season = Season.objects.get(start__lte=dt, end__gte=dt)
    i = stripTime(dt)
    #print(str(i.weekday()) + ", " + str(0))  #str(7 - season.start.weekday()))
    i = i - timedelta(days=i.weekday()) # - timedelta(days=7-season.start.weekday())
    if  i < season.start:
        i = season.start
    return i

@login_required
def home(request):

    # TESTING ONLY    
    try:
        dt = timezone.now() - timedelta(days=67)
        bug_count = 0
        ok        = 0
        while ok < 25:
            
            old_bug_count = bug_count
            
            print(dt.strftime("%c") + ":")
            
            if (bug_count > 20):
                season = Season.objects.get(start__lte=dt, end__gte=dt)
            
            bugs = []

            try:
                wnr = seasonalWeek(dt)
            except ObjectDoesNotExist:
                bugs.append("could not get WNR")
                wnr = None
            
            try:
                sow = startOfSeasonalWeek(dt)
                try:
                    sow_eow = endOfSeasonalWeek(sow)
                except ObjectDoesNotExist:
                    bugs.append("could not get SOW_EOW")
                    sow_eow = None
                try:
                    sow_sow = startOfSeasonalWeek(sow)
                except ObjectDoesNotExist:
                    bugs.append("could not get SOW_SOW")
                    sow_sow = None
                try:
                    sow_wnr = seasonalWeek(sow)
                except ObjectDoesNotExist:
                    bugs.append("could not get SOW_WNR")
                    sow_wnr = None
            except ObjectDoesNotExist:
                bugs.append("could not get SOW")
                sow     = None
                sow_eow = None
                sow_sow = None
                sow_wnr = None

            try:
                eow = endOfSeasonalWeek(dt)
                try:
                    eow_eow = endOfSeasonalWeek(eow)
                except ObjectDoesNotExist:
                    bugs.append("could not get EOW_EOW")
                    eow_eow = None
                try:
                    eow_sow = startOfSeasonalWeek(eow)
                except ObjectDoesNotExist:
                    bugs.append("could not get EOW_SOW")
                    eow_sow = None
                try:
                    eow_wnr = seasonalWeek(eow)
                except ObjectDoesNotExist:
                    bugs.append("could not get EOW_WNR")
                    eow_wnr = None
            except ObjectDoesNotExist:
                bugs.append("could not get EOW")
                eow     = None
                eow_eow = None
                eow_sow = None
                eow_wnr = None

            if sow != sow_sow or sow != eow_sow:
                bugs.append("starts of week do not match")
                bugs.append("\t    SOW: " + (str(    sow) if     sow == None else     sow.strftime("%c")))
                bugs.append("\tSOW_SOW: " + (str(sow_sow) if sow_sow == None else sow_sow.strftime("%c")))
                bugs.append("\tEOW_SOW: " + (str(eow_sow) if eow_sow == None else eow_sow.strftime("%c")))
                
            if eow != sow_eow or eow != eow_eow:
                bugs.append("ends of week do not match")
                bugs.append("\t    EOW: " + (str(    eow) if     eow == None else     eow.strftime("%c")))
                bugs.append("\tSOW_EOW: " + (str(sow_eow) if sow_eow == None else sow_eow.strftime("%c")))
                bugs.append("\tEOW_EOW: " + (str(eow_eow) if eow_eow == None else eow_eow.strftime("%c")))                

            if sow_wnr != eow_wnr or sow_wnr != wnr or eow_wnr != wnr:
                bugs.append("week numbers do not match")
                bugs.append("\t    WNR: " + str(    wnr))
                bugs.append("\tSOW_WNR: " + str(sow_wnr))
                bugs.append("\tEOW_WNR: " + str(eow_wnr))
                
            for bug in bugs:
                print("\tBUG: " + bug)
                bug_count += 1
            
            print("\tWNR: " +  str(wnr)                                        )
            print("\tSOW: " + (str(sow) if sow == None else sow.strftime("%c")))
            print("\tEOW: " + (str(eow) if eow == None else eow.strftime("%c")))
            
            if bug_count > 100:
                raise AssertionError
            
            dt = dt + timedelta(days=1)
            
            if old_bug_count == bug_count:
                ok += 1
    except AssertionError:
        print("\tToo many bugs to continue")
    except ObjectDoesNotExist:
        print("\tCould not get season")
    print("END OF STREAM")
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