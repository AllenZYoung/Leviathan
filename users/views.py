# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm, ChangePWForm, ChangeInfoForm, EvaluateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import timedelta
import re

from . import models
from . import utils

provinces = [u'河北', u'陕西', u'辽宁', u'吉林', u'黑龙江', u'江苏', u'浙江', u'安徽', u'福建', u'江西', u'山东', u'河南', u'湖北', u'湖南', u'广东'
    , u'海南', u'四川', u'贵州', u'云南', u'陕西', u'甘肃', u'青海', u'北京', u'天津', u'上海', u'重庆', u'内蒙古', u'广西', u'宁夏', u'新疆', u'西藏']
provinces.sort()


# 在需要鉴别用户身份的地方，调用request.user.is_authenticated()判断即可
# 需要用户登录才能访问的页面，请添加header @login_required(login_url='users:login'),参见test
# Create your views here.
def index(request):
    province = request.GET.get('province', None)
    if not province:
        province = provinces[0]
        return redirect('/users/?province=' + province)
    cities = utils.get_cities(province)
    city = request.GET.get('city', None)
    if not city:
        location = models.Location.objects.filter(province__contains=province).first()
        if location:
            city = location.city
    hospitals = None
    if city:
        hospitals = utils.get_hospitals(city)
    return render(request, 'users/index.html', {'username': request.user.username, 'provinces': provinces
        , 'cities': cities, 'hospitals': hospitals,'province':province})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'users/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('/users')
            else:
                return HttpResponse('您的账户已被禁用')
        else:
            return render(request, 'users/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form=LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return render(request, 'users/logout.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        valid=form.is_valid()
        print form
        print valid
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            second_password=form.cleaned_data['second_password']
            telephone=form.cleaned_data['telephone']
            email=form.cleaned_data['email']
            name=form.cleaned_data['name']
            idcardnumber=form.cleaned_data['idcardnumber']
            age=form.cleaned_data['age']
            if not username or len(username)<4:
                return render(request, 'users/register.html', {'form': form, 'error_message': '用户名长度不能小于4位！'})
            #用户名查重
            find=models.Patient.objects.filter(username=username).first()
            if find:
                return render(request, 'users/register.html', {'form': form, 'error_message': '用户名已被注册！'})
            if not password or len(password)<4:
                return render(request, 'users/register.html', {'form': form, 'error_message': '密码长度不能小于4位！'})
            if not password == second_password:
                return render(request, 'users/register.html', {'form': form, 'error_message': '两次密码输入不一致!'})
            if email:
                pattern=re.compile('^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$')
                match=pattern.match(email)
                if not match:
                    return render(request, 'users/register.html', {'form': form, 'error_message': '请填写正确的邮箱格式!'})
            if telephone:
                pattern=re.compile('^((\(\d{2,3}\))|(\d{3}\-))?13\d{9}$')
                match=pattern.match(telephone)
                if not match:
                    return render(request, 'users/register.html', {'form': form, 'error_message': '请填写正确的手机号格式!'})
            if not name:
                return render(request, 'users/register.html', {'form': form, 'error_message': '请填写真实姓名!'})
            #身份证格式验证
            pattern=re.compile(r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$')
            match=pattern.match(idcardnumber)
            if not match:
                return render(request, 'users/register.html', {'form': form, 'error_message': '请输入正确的身份证号!'})
            #身份证号查重
            find=models.Patient.objects.filter(idcardnumber=idcardnumber).first()
            if find:
                return render(request, 'users/register.html', {'form': form, 'error_message': '该身份证号已被实名注册，一个身份证号只能注册一个账号!'})
            if not age:
                return render(request, 'users/register.html', {'form': form, 'error_message': '请选择年龄信息!'})
            utils.add_user(form)
            return render(request, 'users/regsuccess.html')
        else:
            return render(request, 'users/register.html', {'form': form, 'error_message': '请输入完整个人信息!'})
    else:
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


class Item:
    doctor = None
    bulletin = None
    department = None
    endtime=None

    def __init__(self, doctor, bulletin, department):
        self.doctor = doctor
        self.bulletin = bulletin
        self.department = department
        self.endtime=bulletin.availabletime + timedelta(hours=4)


def department(request):
    return HttpResponse('department')


def hospital(request):
    hospital_id = request.GET.get('hospital_id', None)
    if not hospital_id:
        return HttpResponse('请先选择医院！')
    department_id = request.GET.get('department_id', None)
    if not department_id:
        department = models.Department.objects.filter(id_hospital=hospital_id).first()
        if department:
            department_id = department.id_department
    hospital = models.Hospital.objects.filter(id_hospital=hospital_id).first()
    location = models.Location.objects.filter(id_location=hospital.id_location.id_location).first()
    departments = models.Department.objects.filter(id_hospital=hospital_id)
    if department_id:
        bulletins = utils.get_bulletins(department_id)
        doctors = utils.get_doctors(bulletins)
        department = models.Department.objects.filter(id_department=department_id).first()
        items = []
        for i in range(len(bulletins)):
            item = Item(doctor=doctors[i], bulletin=bulletins[i], department=department)
            items.append(item)
        return render(request, 'users/hospital.html',
                      {'username': request.user.username, 'hospital': hospital, 'location': location,'departments': departments, 'items': items})
    else:
        return render(request, 'users/hospital.html',
                      {'username': request.user.username, 'hospital': hospital, 'location': location,'departments': departments})


@login_required(login_url='users:login')
def test(request):
    return HttpResponse('Test page')


def doctor(request):
    doctor_id = request.GET.get('doctor_id', 1)
    bulletin_id = request.GET.get('bulletin_id', 1)
    department_id = request.GET.get('department_id', 1)
    doctor = models.Doctor.objects.filter(id_doctor=doctor_id).first()
    bulletin = models.Bulletin.objects.filter(id_bulletin=bulletin_id).first()
    department = models.Department.objects.filter(id_department=department_id).first()
    return render(request, 'users/doctor.html',
                  {'username': request.user.username, 'doctor': doctor, 'bulletin': bulletin
                      , 'department': department})


@login_required(login_url='users:login')
def reservation(request):
    doctor_id = request.GET.get('doctor_id', 1)
    bulletin_id = request.GET.get('bulletin_id', 1)
    department_id = request.GET.get('department_id', 1)
    doctor = models.Doctor.objects.filter(id_doctor=doctor_id).first()
    bulletin = models.Bulletin.objects.filter(id_bulletin=bulletin_id).first()
    department = models.Department.objects.filter(id_department=department_id).first()
    if request.method == 'POST':
        if utils.add_appointment(bulletin, request.user.username):
            return render(request,'users/appdetail.html',{'message':'预约成功'})
        else:
            return render(request,'users/appdetail.html',{'message':'您已成功预约，无需重复预约'})
    return render(request, 'users/reservation.html', {'username': request.user.username
        , 'doctor': doctor, 'bulletin': bulletin, 'department': department})


@login_required(login_url='users:login')
def pay(request):
    return render(request,'users/pay.html')


@login_required(login_url='users:login')
def evaluate(request):
    bulletin_id=request.GET.get('bulletin_id',None)
    patient_id=request.GET.get('patient_id',None)
    # if not bulletin_id:
    #     return HttpResponse('评价医生')
    if request.method=='POST':
        form = EvaluateForm(request.POST)
        if form.is_valid():
            level=form.cleaned_data['level']
            comment=form.cleaned_data['comment']
            utils.add_comment(bulletin_id,patient_id,level,comment)
            return HttpResponse('评价成功')
        else:
            return render(request, 'users/evaluate.html', {'form': form,'message':'请输入正确信息'})
    else:
        form=EvaluateForm()
        return render(request,'users/evaluate.html',{'form':form})


@login_required(login_url='users:login')
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
                                                     'idcn': idcn, 'tel': tele, 'mail': email, 'credit': credit
                                                     })


@login_required(login_url='users:login')
def change_info(request):
    To_change = True
    Bool_changed = False
    if request.method == 'GET':
        form = ChangeInfoForm()
        return render(request, 'users/changeinfo.html', {'form': form, 'To_change': To_change})
    elif request.method == 'POST':
        form = ChangeInfoForm(request.POST)
        if form.is_valid():
            telephone = request.POST.get('telephone', '')
            age = 0  # ugly solution
            if form.cleaned_data['age'] is not None:
                age = request.POST.get('age', '')
            # gender = request.POST.get('gender', '')
            email = request.POST.get('email', '')
            name = request.POST.get('name', '')
            username = request.user.username
            if name != u'':
                utils.change_name(username, name)
                Bool_changed = True
            if telephone != u'':
                utils.change_tel(username, telephone)
                Bool_changed = True
            if email != u'':
                utils.change_email(username, email)
                Bool_changed = True
            if age is not None and int(age) >= 1:
                utils.change_age(username, age)
                Bool_changed = True
            return render(request, 'users/changeinfo.html', {'Bool_changed': Bool_changed, })
            # 'Bool_notchanged':Bool_notchanged})
        return render(request, 'users/changeinfo.html', {'form': form, 'Bool_changed': Bool_changed})


@login_required(login_url='users:login')
def change_pw(request):
    if request.method == 'GET':
        form = ChangePWForm()
        return render(request, 'users/changepwd.html', {'form': form})
    elif request.method == 'POST':
        form = ChangePWForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                utils.change_password(newpassword, username)
                return render(request, 'users/changepwd.html', {'changepwd_success': True})
            else:
                return render(request, 'users/changepwd.html',
                              {'form': form, 'oldpassword_is_wrong': True})
        else:
            return render(request, 'users/changepwd.html', {'form': form})


class Apt:
    patient = None
    doctor = None
    bulletin = None
    department = None
    hospital = None

    def __init__(self, patient, doctor, bulletin, department, hospital):
        self.patient = patient
        self.doctor = doctor
        self.bulletin = bulletin
        self.department = department
        self.hospital = hospital


@login_required(login_url='users:login')
def view_appointment(request):
    username = request.user.username
    patient = models.Patient.objects.filter(username=username).first()
    apps = models.Appointment.objects.filter(id_patient=patient)
    appointments = []
    if apps is not None:
        for app in apps:
            bulletin = app.id_bulletin
            doc_dep = bulletin.id_doctor_department
            doctor = doc_dep.id_doctor
            department = doc_dep.id_department
            hospital = department.id_hospital
            apt = Apt(patient, doctor, bulletin, department, hospital)
            appointments.append(apt)
    return render(request, 'users/viewa.html', {'apps': appointments})
