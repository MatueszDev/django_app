from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm


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