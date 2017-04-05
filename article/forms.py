# -*- coding:utf-8 -*-
# from django.contrib.auth.models import User
from django import forms
from models import User
import datetime


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        initial='',
        label=u'昵称',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'昵称不能包含空格和@字符'}),
    )

    email = forms.EmailField(
        max_length=50,
        initial='',
        label=u'邮箱',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'您的邮箱'}),
    )

    password = forms.CharField(
        min_length=6,
        max_length=18,
        label=u'密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'密码长度为6-18个字符'}),
    )

    confirm_password = forms.CharField(
        min_length=6,
        max_length=18,
        label=u'确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'确认密码'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username or '@' in username:
            raise forms.ValidationError(u'昵称中不能包含空格和@字符')
        res = User.objects.filter(name=username)
        if len(res) != 0:
            raise forms.ValidationError(u'此昵称已经注册，请重新输入')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        res = User.objects.filter(email=email)
        if len(res) != 0:
            raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(u'两次密码输入不一致，请重新输入')

    def save(self):
        name = self.cleaned_data['username']
        email = self.cleaned_data['email']
        psw = self.cleaned_data['password']
        register_time = datetime.datetime.now()
        user = User.objects.create(name=name, email=email, psw=psw, register_time=register_time)
        user.save()
