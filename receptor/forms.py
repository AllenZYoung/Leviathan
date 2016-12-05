# -*- coding: utf-8 -*-
from django import forms


# Forms
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, label='用户名')
    password = forms.CharField(min_length=4, label='密码',widget=forms.PasswordInput())
    second_password = forms.CharField(min_length=4, label='再次输入密码',widget=forms.PasswordInput())
    hospital=forms.IntegerField(label='医院id')



class LoginForm(forms.Form):
    username=forms.CharField(min_length=4, label='用户名')
    password = forms.CharField(min_length=4, label='密码', widget=forms.PasswordInput())