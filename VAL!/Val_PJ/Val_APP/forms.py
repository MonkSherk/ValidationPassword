from django import forms
from django.core.exceptions import ValidationError
import re


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise ValidationError("Имя пользователя должно содержать не менее 3 символов.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'spam' in email:
            raise ValidationError("Адрес электронной почты не должен содержать слово 'spam'.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать не менее 8 символов.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not re.search(r'[\W_]', password):
            raise ValidationError("Пароль должен содержать хотя бы один специальный символ.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError("Пароли не совпадают.")
        return cleaned_data
