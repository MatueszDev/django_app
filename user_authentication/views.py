from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            id = new_user.id
            text = "Hi!\nHow are you?\nHere is the link to activate your account:\n" \
                   "http://localhost:8000/activation/?id=%s" %id
            subject = "Activate your account at Student Notebook"
            send_mail(subject, text, 'admin@myblog.com', [register_form.cleaned_data['email']])
            return render(request, 'user_authentication/thankyou.html')
    else:
        register_form = UserRegistrationForm()
    return render(request, 'user_authentication/register.html', {'register_form': register_form})


def activate(request):
    id = int(request.GET.get('id'))
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return render(request, 'user_authentication/activation.html')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'user_authentication/edit_done.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'user_authentication/edit.html', {'user_form': user_form,  'profile_form': profile_form})


