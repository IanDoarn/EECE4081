from django.shortcuts import render
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

#def throwaway(request):
    
    #try:
    #    usermail = request.GET['usermail']
    #    password = request.GET['password']
    #except MultiValueDictKeyError:
    #    return render(request, 'login.html')
    
    #print(usermail)
    #print(password)
    
    #return render(request, 'index.html')

from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login, authenticate
from django.urls.exceptions import NoReverseMatch
    
def LoginView(request):
    if request.user.is_anonymous or ~request.user.is_authenticated:
        try:
            username = request.GET['username']
            password = request.GET['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
        except MultiValueDictKeyError:
            pass   
    if request.user.is_authenticated and ~request.user.is_anonymous:
        try:
            return redirect(request.GET['next'])
        except MultiValueDictKeyError:
            return redirect('/accounts/profile/')
        except NoReverseMatch:
            return redirect('/accounts/profile/')
    return render(request, 'registration/login.html')
    
def ProfileView(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login/?next=' + request.path)
        #return render(request, 'registration/login.html')
        #return HttpResponseRedirect('/accounts/login/', {'next':request.path})
    return render(request, 'profile.html')
