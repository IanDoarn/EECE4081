from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Game, Bet
from datetime import date, datetime, timedelta

fdow = lambda: datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)

@login_required
def home(request):
    table_headers = ['Favorite', 'Line', 'Underdog', 'TV', 'Date / Time']

    games = Game.objects.filter(date_time__range=(
        fdow(), fdow() + timedelta(days=7)
    )).order_by('date_time')

    bets = Bet.objects.filter(date_time__range=(
        fdow(), fdow() + timedelta(days=7)
    ))




    return render(request, 'home.html', {'games': games, 'table_headers': table_headers})


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