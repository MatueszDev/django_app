from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    email = forms.CharField(disabled="disabled")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        help_texts = {'date_of_birth': 'date format: YYYY-MM-DD'}
        fields = ('date_of_birth', 'subjects')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=64, label='Username', help_text=None)
    first_name = forms.CharField(required=True, max_length=64, label='First Name', help_text=None)
    last_name = forms.CharField(required=True, max_length=64, label='Last Name', help_text=None)
    email = forms.CharField(required=True, max_length=64, label='Email',
                            help_text='Please provide your student email - fis.agh.edu.pl')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput, min_length=8,
                               help_text='Password should be at least 8 characters')
    password_2 = forms.CharField(required=True, label='Repeat password', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean_email(self):
        if self.cleaned_data['email'].find("fis.agh.edu.pl") == -1:
            raise forms.ValidationError('You provided wrong email')

        email = self.cleaned_data['email']
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')

    def clean_password_2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_2']:
            raise forms.ValidationError('Passwords do not match. Please, provide password again.')
        return self.cleaned_data['password_2']



