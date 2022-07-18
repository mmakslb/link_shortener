from django import forms
from .models import Shortener
from django.utils import timezone
from django.contrib.auth.models import User


class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "ENTER THE LINK HERE"}))

    class Meta:
        model = Shortener
        fields = ('long_url',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = (self.cleaned_data['username']).lower()
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('The username or password is incorrect!')
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('The username or password is incorrect!')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=8, widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    first_name = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'
        self.fields['password_check'].label = 'Repeat Password'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'Name'

    def clean(self):
        username = (self.cleaned_data['username']).lower()
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The user with this login is already registered in the system!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The user with this email is already registered in the system!')
        if password != password_check:
            raise forms.ValidationError('Your passwords do not match! Try again!')
