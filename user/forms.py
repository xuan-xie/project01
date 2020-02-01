from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={

                                   'class' :"form-control required",
                                   'id':'username',
                                   'autofocus':"autofocus",
                                   'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                                min_length=4,
                                max_length=20,
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control required",
                                    'id':'password',
                                    'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if not user is None:
            self.cleaned_data['user'] = user
            return self.cleaned_data
        else:
            raise forms.ValidationError('账号密码错误')



class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'id': 'email',
                                                             'for': 'email',
                                                             'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               min_length=4,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'id': 'password',
                                                                 'for': 'email',
                                                                 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='确认密码',
                               min_length=4,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': '确认密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已经存在')
        return username

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError('两次密码输入不一致')
        return password



