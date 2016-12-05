# coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from users import  models
from utils import findAppByRP,addUser,findAppByUser

import datetime
# Create your views here.

def index(request):
    if request.session.get('isLogin', False):
        return render(request,'receptor/index.html',{'username':request.session['userName']})
    else:
        return render(request, 'receptor/index.html',{'username':False})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['password'] == form.cleaned_data['second_password']:
                form = RegisterForm()
                return render(request, 'receptor/register.html', {'form': form, 'error_message': '两次密码输入不一致!'})
            else:
                addUser(form)
                return render(request, 'receptor/regsuccess.html')
        else:
            form = RegisterForm()
            return render(request, 'receptor/register.html', {'form': form, 'error_message': '请输入正确信息!'})
    else:
        form = RegisterForm()
        return render(request, 'receptor/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            form = LoginForm()
            return render(request, 'receptor/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = models.Adminreceptor.objects.get(loginname=username,password=password)
        if user is not None:
            request.session['userId']=user.id_adminreceptor
            request.session['userName']=user.loginname
            request.session['isLogin']=True
            return HttpResponse("success")
        else:
            form = LoginForm()
            return render(request, 'receptor/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form = LoginForm()
        return render(request, 'receptor/login.html', {'form': form})


def logout(request):
    del request.session['isLogin']
    del request.session['userId']
    return HttpResponse('注销成功')

def showAppoint(request,param1):
    if request.session.get('isLogin',False):
        userId = request.session['userId']
        appointments = findAppByRP(userId)
        if param1 is not None:
            if (param1.lower()=="toshow"):
                return render(request, 'receptor/ToShow.html', {'appointments': appointments})
            elif (param1.lower()=='isshowned') :
                return render(request, 'receptor/appointmentsIsShowned.html', {'appointments': appointments})
            else:
                return render(request, 'receptor/showAppointments.html', {'appointments': appointments})
        else:
            return render(request, 'receptor/showAppointments.html', {'appointments': appointments})
    else:
        form = LoginForm()
        return redirect('/receptor/login', {'form': form, 'error_message': '请登录'})

def showPatient(request,name):
    if request.session.get('isLogin', False):
        appointments=findAppByUser(name)
        return render(request,'receptor/patient.html',{'appointments':appointments})
    else:
        form = LoginForm()
        return redirect('/receptor/login', {'form': form, 'error_message': '请登录'})

def confirmAppointment(request):
    if request.session.get('isLogin',False):
        id=request.GET['id']
        appointment=models.Appointment.objects.get(id_appointment=id)
        appointment.ispaid=True
        appointment.registrationtime=datetime.datetime.now()
        appointment.save(force_update=True)
        return  render(request,'receptor/confirmAppointment.html',{'time':appointment.registrationtime})

def printAppointment(request):
    return render(request,'receptor/printAppointment.html')
