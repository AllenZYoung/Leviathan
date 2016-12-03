# -*- coding: utf-8 -*-
from django import forms


# Forms
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, label='用户名')
    password = forms.CharField(min_length=4, label='密码', widget=forms.PasswordInput())
    second_password = forms.CharField(min_length=4, label='再次输入密码', widget=forms.PasswordInput())
    telephone = forms.CharField(required=False, label='手机号(选填)')
    email = forms.EmailField(required=False, label='邮箱(选填)', widget=forms.EmailInput())
    name = forms.CharField(label='真实姓名')
    # debug mode
    idcardnumber = forms.CharField(max_length=18, label='18位合法身份证号')
    GENDER = (
        (0, '男'),
        (1, '女')
    )
    gender = forms.ChoiceField(choices=GENDER, label='性别')
    age = forms.IntegerField(min_value=0, max_value=150, label='年龄')


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, label='用户名')
    password = forms.CharField(min_length=4, label='密码', widget=forms.PasswordInput())


class ChangePWForm(forms.Form):
    oldpassword = forms.CharField(max_length=32, label='旧密码')
    newpassword1 = forms.CharField(max_length=32, label='新密码')
    newpassword2 = forms.CharField(max_length=32, label='确认密码')

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangePWForm, self).clean()
        return cleaned_data
