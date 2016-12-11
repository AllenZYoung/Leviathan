# -*- coding: utf-8 -*-
from django import forms


# Forms
class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'class': 'form-control input-circle', 'placeholder': '登录名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control input-circle', 'placeholder': '密码'}))
    second_password = forms.CharField(label='再次输入密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control input-circle', 'placeholder': '再次输入密码'}))
    telephone = forms.CharField(required=False, label='手机号(选填)',
                                widget=forms.TextInput({'class': 'form-control input-circle', 'placeholder': '手机号'}))
    email = forms.EmailField(required=False, label='邮箱(选填)',
                             widget=forms.TextInput(attrs={'class': 'form-control input-circle', 'placeholder': '邮箱'}))
    name = forms.CharField(label='真实姓名',
                           widget=forms.TextInput(attrs={'class': 'form-control input-circle', 'placeholder': '姓名'}))
    idcardnumber = forms.CharField(label='18位合法身份证号', widget=forms.TextInput(
        attrs={'class': 'form-control input-circle', 'placeholder': '18位身份证号'}))
    GENDER = (
        (0, '男'),
        (1, '女')
    )
    gender = forms.ChoiceField(choices=GENDER, label='性别')
    age = forms.IntegerField(min_value=0, max_value=150, label='年龄',
                             widget=forms.TextInput(attrs={'class': 'form-control input-circle', 'placeholder': '年龄'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-solid placeholder-no-fix', 'placeholder': '请输入用户名', }))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-solid placeholder-no-fix', 'placeholder': '请输入密码', }))


class ChangePWForm(forms.Form):
    oldpassword = forms.CharField(max_length=32, label='旧密码'
                                  , widget=forms.PasswordInput(attrs={'class': 'form-control input-circle', 'placeholder': '旧密码'}))
    newpassword1 = forms.CharField(max_length=32, label='新密码',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control input-circle', 'placeholder': '新密码'}))
    newpassword2 = forms.CharField(max_length=32, label='确认密码',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control input-circle', 'placeholder': '再次输入新密码'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangePWForm, self).clean()
        return cleaned_data


class ChangeInfoForm(forms.Form):
    telephone = forms.CharField(required=False, label='手机号(选填)'
                                , widget=forms.TextInput(attrs={'class': 'form-control input-circle', 'placeholder': '手机号'}))
    email = forms.EmailField(required=False, label='邮箱(选填)',
                             widget=forms.EmailInput(attrs={'class': 'form-control input-circle', 'placeholder': '邮箱'}))
    name = forms.CharField(required=False, label='真实姓名',
                           widget=forms.TextInput(attrs={'class': 'form-control input-circle', 'placeholder': '姓名'}))
    age = forms.IntegerField(required=False, min_value=0, max_value=150, label='年龄',
                             widget=forms.TextInput(attrs={'class': 'form-control input-circle', 'placeholder': '年龄'}))


class EvaluateForm(forms.Form):
    LEVEL = (
         (5, '很好'),(4, '好'), (3, '一般'),(2, '不好'),  (1, '很不好'),
    )
    level = forms.ChoiceField(choices=LEVEL, label='评价等级')
    comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'8'}), label='写下你对医生的评价', required=False)
