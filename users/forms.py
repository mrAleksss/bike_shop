from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()

    # username = forms.CharField(label="Ім'я користувача", widget=forms.TextInput(attrs={"autofocus": True,
    #                                                          'class': 'form-control',
    #                                                          'placeholder': "Введіть ім'я користувача"}))
    # password = forms.CharField(label="Пароль",
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                       'class': 'form-control',
    #                                       'placeholder': 'Введіть пароль'}),
    # )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password1', 
            'password2')
        
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control', 
    #             'placeholder': "Введіть ваше ім'я"}))
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control', 
    #             'placeholder': 'Введіть ваше прізвище'}))
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attres={
    #             'class': 'form-control', 
    #             'placeholder': 'Введіть ваш нікнейм'}))
    # email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             'class': 'form-control', 
    #             'placeholder': 'Введіть ваш email *youremail@example.com'}))
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control', 
    #             'placeholder': 'Введіть ваш пароль'}))
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control', 
    #             'placeholder': 'Підтвердіть ваш пароль'}))



