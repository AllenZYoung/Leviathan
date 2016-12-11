# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Patient(models.Model):
    id_patient = models.AutoField(null=False, primary_key=True, max_length=11)
    username = models.CharField(null=False, unique=True, max_length=15, help_text='用户名，用于登陆')
    password = models.CharField(null=False, max_length=32, )
    telephone = models.CharField(null=False, blank=True, max_length=15, help_text='选填，用于备案')
    email = models.EmailField(help_text='选填，用于备案', max_length=50, blank=True)
    name = models.CharField(null=False, max_length=45, help_text='认证实名')
    CREDIT_LEVEL = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('X', 'X')
    )
    credit = models.CharField(null=False, choices=CREDIT_LEVEL, help_text='信用额度', max_length=1)
    idcardnumber = models.CharField(null=False, max_length=18, unique=True, help_text='身份证号定长18位')
    GENDER = (
        ('男', '男'),
        ('女', '女')
    )
    gender = models.CharField(null=False, choices=GENDER, max_length=1)
    age = models.IntegerField(null=False, default=0)
    createtime = models.DateTimeField(help_text='注册时间', max_length=100, null=True, blank=True)

    # change table name, remove prefix 'users'
    class Meta:
        db_table = 'patient'

    # tostring
    def __str__(self):
        return 'username: %s id: %s' % (self.username, self.id_patient)

    def __unicode__(self):
        return u'username: %s id: %s' % (self.username, self.id_patient)


class Location(models.Model):
    id_location = models.AutoField(null=False, primary_key=True, max_length=11)
    province = models.CharField(null=True, max_length=20, help_text='省/自治区(直辖市和特别行政区留白', blank=True)
    city = models.CharField(null=False, max_length=20, help_text='市')
    county = models.CharField(null=False, max_length=20, help_text='主城区/县')
    street = models.CharField(null=True, max_length=50, help_text='街道地址门牌号', blank=True)

    def __str__(self):
        return 'province: %s  city: %s  street: %s' % (self.province, self.city, self.street)

    def __unicode__(self):
        return u'province: %s  city: %s  street: %s' % (self.province, self.city, self.street)

    class Meta:
        db_table = 'location'


class Hospital(models.Model):
    id_hospital = models.AutoField(null=False, primary_key=True, max_length=11)
    id_location = models.ForeignKey(Location, to_field='id_location', on_delete=models.CASCADE, db_column='id_location')
    name = models.CharField(null=False, max_length=45)
    LEVEL = (
        ('一级丙等', '一级丙等'), ('一级乙等', '一级乙等'), ('一级甲等', '一级甲等'), ('二级丙等', '二级丙等'), ('二级乙等', '二级乙等'),
        ('二级甲等', '二级甲等'), ('三级丙等', '三级丙等'), ('三级乙等', '三级乙等'), ('三级甲等', '三级甲等'), ('三级特等', '三级特等')
    )
    level = models.CharField(null=False, choices=LEVEL, max_length=20)
    TYPE = (
        ('普通', '普通'), ('专科', '专科')
    )
    type = models.CharField(null=True, choices=TYPE, max_length=20, help_text='医疗服务是否专科', blank=True, default='普通')
    information = models.TextField(blank=True, default='无说明信息')
    telephone = models.CharField(null=True, max_length=15, blank=True)
    picture = models.CharField(null=True, max_length=90, help_text='医院照片，存路径', blank=True)
    createtime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return ': %s  level: %s' % (self.name, self.level)

    def __unicode__(self):
        return u': %s  level: %s' % (self.name, self.level)

    class Meta:
        db_table = 'hospital'


class Doctor(models.Model):
    id_doctor = models.AutoField(null=False, primary_key=True, max_length=11)
    name = models.CharField(null=False, help_text='医生实名', max_length=45)
    LEVEL = (
        ('主任医师', '主任医师'), ('副主任医师', '副主任医师'), ('主治医师', '主治医师'), ('住院医师', '住院医师')
    )
    level = models.CharField(null=False, choices=LEVEL, max_length=10)
    information = models.TextField(null=True, blank=True)
    picture = models.CharField(null=True, max_length=90, help_text='医生照片，存路径', blank=True)
    speciality = models.CharField(null=True, max_length=90, help_text='主治特长', blank=True)
    careertime = models.IntegerField(null=False, default=0, help_text='医龄，单位为年')
    GENDER = (
        ('男', '男'),
        ('女', '女')
    )
    gender = models.CharField(null=False, choices=GENDER, max_length=10)
    age = models.IntegerField(null=False, default=0)
    createtime = models.DateTimeField(help_text='生成时间', null=True, blank=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return 'doctor name: %s' % self.name

    def __unicode__(self):
        return u'doctor name: %s' % self.name


class Department(models.Model):
    id_department = models.AutoField(null=False, primary_key=True, max_length=11)
    id_hospital = models.ForeignKey(Hospital, to_field='id_hospital', on_delete=models.CASCADE, db_column='id_hospital')
    name = models.CharField(null=False, max_length=45)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    information = models.TextField(null=True, blank=True, help_text='概述')

    class Meta:
        db_table = 'department'

    def __str__(self):
        return 'department name: %s' % self.name

    def __unicode__(self):
        return u'department name: %s' % self.name


class DoctorDepartment(models.Model):
    id_doctor_department = models.AutoField(null=False, primary_key=True, max_length=11)
    id_doctor = models.ForeignKey(Doctor, to_field='id_doctor', null=False, db_column='id_doctor')
    id_department = models.ForeignKey(Department, to_field='id_department', null=False, db_column='id_department')

    class Meta:
        db_table = 'doctor_department'

    def __str__(self):
        return 'doctor id: %s     department id: %s' % (self.id_doctor, self.id_department)

    def __unicode__(self):
        return u'doctor id: %s     department id: %s' % (self.id_doctor, self.id_department)


class Adminreceptor(models.Model):
    id_adminreceptor = models.AutoField(null=False, primary_key=True, max_length=11)
    id_hospital = models.ForeignKey(Hospital, to_field='id_hospital', db_column='id_hospital')
    loginname = models.CharField(max_length=45, null=False, unique=True, help_text='登陆标识符，实际可为自定义用户名或院方定义的用户名(比如工号)')
    password = models.CharField(max_length=32, null=False)
    createtime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'adminreceptor'

    def __str__(self):
        return 'Adminreceptor  loginname: %s' % self.loginname

    def __unicode__(self):
        return u'Adminreceptor  loginname: %s' % self.loginname


class Adminpublisher(models.Model):
    id_adminpublisher = models.AutoField(null=False, primary_key=True, max_length=11)
    id_hospital = models.ForeignKey(Hospital, to_field='id_hospital', db_column='id_hospital')
    loginname = models.CharField(max_length=45, null=False, unique=True, help_text='登陆标识符，实际可为自定义用户名或被注册受理方给定的用户名')
    password = models.CharField(max_length=32, null=False)
    telephone = models.CharField(max_length=15, null=True, help_text='或许用于备案存档的信息', blank=True)
    email = models.EmailField(help_text='选填，用于备案', max_length=50, null=True, blank=True)
    createtime = models.DateTimeField(help_text='注册事件', null=True, blank=True)

    class Meta:
        db_table = 'adminpublisher'

    def __str__(self):
        return 'adminpublisher loginname: %s' % self.loginname

    def __unicode__(self):
        return u'adminpublisher loginname: %s' % self.loginname


class Bulletin(models.Model):
    id_bulletin = models.AutoField(null=False, primary_key=True, max_length=11)
    id_adminpublisher = models.ForeignKey(Adminpublisher, to_field='id_adminpublisher', help_text='发布者',
                                          db_column='id_adminpublisher')
    id_doctor_department = models.ForeignKey(DoctorDepartment, to_field='id_doctor_department', help_text='可预约的医生',
                                             db_column='id_doctor_department')
    availabletime = models.DateTimeField(null=False, help_text='可预约时间段')
    fee = models.FloatField(null=False, default=0, help_text='(预约)挂号费')
    countavailable = models.IntegerField(null=False, help_text='初始声明的可预约数量')
    countoccupied = models.IntegerField(null=False, help_text='已预约数量')
    createtime = models.DateTimeField(help_text='最后一次新增预约记录的时间', null=True, blank=True)

    class Meta:
        db_table = 'bulletin'

    def __str__(self):
        return 'bulletin id: %s' % self.id_bulletin

    def __unicode__(self):
        return u'bulletin id: %s' % self.id_bulletin


class Appointment(models.Model):
    id_appointment = models.AutoField(null=False, primary_key=True, max_length=11)
    id_patient = models.ForeignKey(Patient, to_field='id_patient', db_column='id_patient')
    id_bulletin = models.ForeignKey(Bulletin, to_field='id_bulletin', help_text='分诊台操作员从这里取得预约信息',
                                    db_column='id_bulletin')
    ispaid = models.BooleanField(null=False, default='0')
    registrationtime = models.DateTimeField(help_text='到院取号时间-此项说明了是否爽约', null=True, blank=True)
    createtime = models.DateTimeField(help_text='预约单生成时间', null=False)

    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return 'appointment id: %s' % self.id_appointment

    def __unicode__(self):
        return u'appointment id: %s' % self.id_appointment


class Evaluation(models.Model):
    id_evaluation=models.AutoField(null=False, primary_key=True, max_length=11)
    patient=models.ForeignKey(Patient, to_field='id_patient', db_column='patient')
    doctor=models.ForeignKey(Doctor, to_field='id_doctor', db_column='doctor')
    level=models.IntegerField(null=True,blank=True,help_text='医生评价等级')
    comment=models.TextField(null=True,blank=True,help_text='医生评价',default='暂无评价信息')
    #createtime = models.DateTimeField(help_text='评价成时间', null=False)

    class Meta:
        db_table='evaluation'

        def __str__(self):
            return 'evaluation id: %s' % self.id_evaluation

        def __unicode__(self):
            return u'evaluation id: %s' % self.id_evaluation