# -*- coding: utf-8 -*-
# 功能函数放置在此文件中
# from forms import LoginForm, RegisterForm
from django.db import models
from users import models
import datetime
from openpyxl.reader.excel import load_workbook
import os
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def add_publisher(form):
    data = form.cleaned_data
    publisher = models.Adminpublisher.objects.create(loginname=data['loginname'],
                                                     password=data['password'],
                                                     telephone=data['telephone'],
                                                     email=data['email'],
                                                     createtime=datetime.datetime.now(),
                                                     id_hospital_id=data['hospital'])


def auth_publisher(form):
    if form.is_valid():
        data = form.cleaned_data
        loginname = data['loginname']
        password = data['password']
        # check
        publisher = models.Adminpublisher.objects.filter(loginname=loginname, password=password)
        # print publisher
        return publisher
    else:
        return None


def select_hospital():
    hospital = models.Hospital.objects.all().values('id_hospital', 'name')
    h_list=[]
    if hospital:
        for h_dict in hospital:
            t_tuple = (h_dict['id_hospital'], h_dict['name'])
            h_list.append(t_tuple)
    return h_list


def publisher_exists(name):
    publisher = models.Adminpublisher.objects.filter(loginname=name)
    if publisher:
        return True
    return False


def select_all_bulletin(hospital_id):
    bulletins = models.Bulletin.objects.filter(id_adminpublisher__id_hospital_id=hospital_id)
    return bulletins


def handle_uploaded_file(request, f=None):
    datenow = datetime.datetime.now()
    filedate = datenow.strftime('%Y%m%d-%H%M%S')
    path = os.path.join(os.path.abspath('.'),'publisher','fileUpload')
    filepath = path + '/' + filedate + '_' + f.name
    with open(filepath, 'ab') as de:
        for chunk in f.chunks():
            de.write(chunk)
    wb = load_workbook(filepath)
    print filepath
    table = wb.get_sheet_by_name(wb.get_sheet_names()[0])
    # print table.max_row
    # print table.max_column
    bulletin_list = []
    for i in range(2, table.max_row + 1):
        if table.cell(row=i, column=1).value is None:
            # print '科室为空，应跳过'
            continue
        print '正在导入第' + str(i - 1) + '行...'
        bulletin = models.Bulletin(
            availabletime=table.cell(row=i, column=3).value,
            countavailable=table.cell(row=i, column=4).value,
            countoccupied=table.cell(row=i, column=5).value,
            fee=table.cell(row=i, column=6).value,
            createtime=datetime.datetime.now(),
            id_adminpublisher_id=1,
            id_doctor_department_id=_get_id_doctor_department(request, dept_name=table.cell(row=i, column=1).value, dt_name=table.cell(row=i, column=2).value)
        )
        bulletin_list.append(bulletin)
    models.Bulletin.objects.bulk_create(bulletin_list)
    print bulletin_list


def _get_id_doctor_department(request, dept_name, dt_name):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        doc_dept = models.DoctorDepartment.objects.get(id_department__name=dept_name,
                                                       id_department__id_hospital_id=request.session['hospital_id'],
                                                       id_doctor__name=dt_name)
        print doc_dept
        return doc_dept.id_doctor_department
    except MultipleObjectsReturned, e:
        print('科室：%s,医生：%s组合不止一个！' % (dept_name, dt_name))
        print e
        raise RuntimeError
        #return None
    except ObjectDoesNotExist, e:
        print('不存在科室：%s,医生：%s组合！' % (dept_name, dt_name))
        print e
        raise RuntimeError
        return None
