from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('You are logged in.')
                else:
                    return HttpResponse('Sorry, your account seems to be blocked.')
            else:
                return HttpResponse('Please check if you provided proper username and password.')
    else:
        form = LoginForm()
    return render(request, 'user_authentication/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'user_authentication/register_done.html', {'new_user': new_user})
    else:
        register_form = UserRegistrationForm()
    return render(request, 'user_authentication/register.html', {'register_form': register_form})