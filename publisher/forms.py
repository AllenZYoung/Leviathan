# -*- coding: utf-8 -*-
from django import forms
from . import utils


# Forms
class LoginForm(forms.Form):
    loginname=forms.CharField(min_length=4, label='用户名')
    password = forms.CharField(min_length=4, label='密码', widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    loginname = forms.CharField(required=True, min_length=4, label='管理员登录名')
    password = forms.CharField(required=True, min_length=4, label='密码',widget=forms.PasswordInput())
    second_password = forms.CharField(required=True, min_length=4, label='再次输入密码',widget=forms.PasswordInput())
    telephone = forms.CharField(required=False, label='手机号(选填)')
    email = forms.EmailField(required=False, label='邮箱(选填)',widget=forms.EmailInput())
    hospital = forms.ChoiceField(required=True, label='所属医院', widget=forms.Select(),
                                 choices=utils.select_hospital())


class FileForm(forms.Form):
    filefield = forms.FileField(required=True, label='请选择文件')
    # filepath = forms.FilePathField(required=True, label='请选择文件路径')
