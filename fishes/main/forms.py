from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=64)
    password = forms.CharField(label='Пароль', max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    blog_title = forms.CharField(label='Название блога', max_length=80)
    username = forms.CharField(label='Логин', max_length=64)
    email = forms.EmailField(label='E-Mail', max_length=128)
    password = forms.CharField(label='Пароль', min_length=3, max_length=128, widget=forms.PasswordInput)
    password_again = forms.CharField(label='Повторите пароль', min_length=3, max_length=128, widget=forms.PasswordInput)
