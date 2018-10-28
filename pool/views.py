from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Game, Bet
from datetime import date, datetime, timedelta
from django.utils import timezone

fdow = lambda: datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)

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

@login_required
def home(request):

    games = Game.objects.filter(date_time__range=(
        mondayOfSameWeek(timezone.now()), # lastWeek(timezone.now())
        sundayOfSameWeek(timezone.now())  # lastWeek(timezone.now())
                                          # todo: replace with comments
    ))
    game_ids = []
    for game in games:
        game_ids.append(game.id)
    bets = Bet.objects.filter(game_id__in=game_ids)
    points = {}
    for bet in bets:
        try:
            value = points[bet.user_id]
        except KeyError:
            value = 0
        if bet.game_id.underdog_score != None and bet.game_id.favorite_score != None:
            if bet.team_id == bet.game_id.underdog_id:
                if bet.game_id.favorite_score < (bet.game_id.underdog_score + bet.game_id.spread):
                    value = value + 1
            else:
                if bet.game_id.underdog_score < (bet.game_id.favorite_score - bet.game_id.spread):
                    value = value + 1
        points[bet.user_id] = value
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
                        
    return render(
        request, 'home.html',
        {
            'games': Game.objects.filter(date_time__range=(
                        mondayOfSameWeek(timezone.now()),
                        sundayOfSameWeek(timezone.now())
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