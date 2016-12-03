# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm,ChangePWForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from . import models
from . import utils

provinces = ['河北', '陕西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东'
    , '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '北京', '天津', '上海', '重庆', '内蒙古', '广西', '宁夏', '新疆', '西藏']
provinces.sort()


# 在需要鉴别用户身份的地方，调用request.user.is_authenticated()判断即可
# 需要用户登录才能访问的页面，请添加header @login_required(login_url='login'),参见test
# Create your views here.
def index(request):
    province = request.GET.get('province', None)
    city = request.GET.get('city', None)
    hospitals = None
    cities = None
    if city:
        hospitals = utils.getHospitals(city)
    elif province:
        cities = utils.getCities(province)
    return render(request, 'users/index.html', {'username': request.user.username, 'provinces': provinces
        , 'cities': cities, 'hospitals': hospitals})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            form = LoginForm()
            return render(request, 'users/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('/users')
            else:
                return HttpResponse('您的账户已被禁用')
        else:
            form = LoginForm()
            return render(request, 'users/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return render(request,'users/logout.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['password'] == form.cleaned_data['second_password']:
                form = RegisterForm()
                return render(request, 'users/register.html', {'form': form, 'error_message': '两次密码输入不一致!'})
            else:
                utils.addUser(form)
                return render(request, 'users/regsuccess.html')
        else:
            form = RegisterForm()
            return render(request, 'users/register.html', {'form': form, 'error_message': '请输入正确信息!'})
    else:
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


class Item:
    doctor=None
    bulletin=None
    department=None

    def __init__(self,doctor,bulletin,department):
        self.doctor=doctor
        self.bulletin=bulletin
        self.department=department


def department(request):
    return HttpResponse('department')


def hospital(request):
    hospital_id = request.GET.get('hospital_id', None)
    department_id=request.GET.get('department_id',None)
    hospital = models.Hospital.objects.filter(id_hospital=hospital_id).first()
    departments = models.Department.objects.filter(id_hospital=hospital_id)
    if department_id:
        location = models.Location.objects.filter(id_location=hospital.id_location.id_location).first()
        bulletins=utils.getBulletins(department_id)
        doctors=utils.getDoctors(bulletins)
        department=models.Department.objects.filter(id_department=department_id).first()
        items=[]
        for i in range(len(bulletins)):
            item=Item(doctor=doctors[i],bulletin=bulletins[i],department=department)
            items.append(item)
        return render(request, 'users/hospital.html',
                      {'username': request.user.username, 'hospital': hospital, 'location': location,'departments':departments,'items':items})
    else:
        return render(request,'users/hospital.html',{'username': request.user.username, 'hospital': hospital,'departments':departments})



@login_required(login_url='login')
def test(request):
    return HttpResponse('Test page')


def doctor(request):
    doctor_id=request.GET.get('doctor_id',1)
    bulletin_id=request.GET.get('bulletin_id',1)
    department_id=request.GET.get('department_id',1)
    doctor=models.Doctor.objects.filter(id_doctor=doctor_id).first()
    bulletin=models.Bulletin.objects.filter(id_bulletin=bulletin_id).first()
    department=models.Department.objects.filter(id_department=department_id).first()
    return render(request,'users/doctor.html',{'username':request.user.username,'doctor':doctor,'bulletin':bulletin
        ,'department':department})


@login_required(login_url='login')
def reservation(request):
    doctor_id = request.GET.get('doctor_id', 1)
    bulletin_id = request.GET.get('bulletin_id', 1)
    department_id = request.GET.get('department_id', 1)
    doctor = models.Doctor.objects.filter(id_doctor=doctor_id).first()
    bulletin = models.Bulletin.objects.filter(id_bulletin=bulletin_id).first()
    department = models.Department.objects.filter(id_department=department_id).first()
    if request.method=='POST':
        if utils.addAppointment(bulletin,request.user.username):
            return HttpResponse('预约成功')
        else:
            return HttpResponse('您已成功预约，无需重复预约')
    return render(request,'users/reservation.html',{'username':request.user.username
        ,'doctor':doctor,'bulletin':bulletin,'department':department})


@login_required(login_url='login')
def user_center(request):
    username = request.user.username
    # print(username)
    # userhere = models.Patient.objects.filter(username='useruser').first()
    # it should be :
    userhere = models.Patient.objects.filter(username=username).first()
    # print(userhere)
    name = userhere.name
    sex = userhere.gender
    age = userhere.age
    idcn = userhere.idcardnumber
    tele = userhere.telephone
    email = userhere.email
    credit = userhere.credit
    return render(request, 'users/usercenter.html', {'wholename': name, 'sex': sex, 'age': age,
    'idcn':idcn,'tel':tele,'mail':email,'credit':credit
    })

@login_required(login_url='login')
def change_info(request):
    pass

@login_required(login_url='login')
def change_pw(request):
    if request.method == 'GET':
        form = ChangePWForm()
        return render(request,'users/changepwd.html', {'form': form})
    elif request.method == 'POST':
        form = ChangePWForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                utils.change_password(newpassword,username)
                return render(request,'users/changepwd.html', {'changepwd_success': True})
            else:
                return render(request,'users/changepwd.html',
                                         {'form': form, 'oldpassword_is_wrong': True})
        else:
            return render(request,'users/changepwd.html', {'form': form})

@login_required(login_url='login')
def view_appointment(request):
    pass