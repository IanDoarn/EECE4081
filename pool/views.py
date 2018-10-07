from django.shortcuts import render
from random import choice

def home(request):
    greetings = ['Hello, ', 'Welcome Back, ', 'Hi, ', 'Welcome, ']
    return render(request, 'pool/home.html', {'title': 'Home', 'current_user': choice(greetings) + 'Ian Doarn' + '...'})