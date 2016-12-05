from users import models
import datetime

def findAppByRP(userID):
    receptor=models.Adminreceptor.objects.get(id_adminreceptor=userID)
    hospitalID=receptor.id_hospital
    today=datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    departmentList=list(models.Department.objects.filter(id_hospital=hospitalID))
    appDicList=[]
    for i in departmentList:
        docDepList=list(models.DoctorDepartment.objects.filter(id_department=i.id_department))
        for j in docDepList:
            bulletinList=list(models.Bulletin.objects.filter(id_doctor_department=j.id_doctor_department).filter(availabletime__range=(today,tomorrow)))
            for k in bulletinList:
                appointmentList=list(models.Appointment.objects.filter(id_bulletin=k.id_bulletin))
                for l in appointmentList:
                    if l is not None:
                        regiistrationtime=l.registrationtime
                        if regiistrationtime is not None:
                            appDic = {'anAppointment': l, 'patient': l.id_patient, 'doctor': j.id_doctor,
                                      'department': i, 'time': k.availabletime, 'fee': k.fee, 'isShow': True}
                            appDicList.append(appDic)
                        else:
                            appDic = {'anAppointment': l, 'patient': l.id_patient, 'doctor': j.id_doctor,
                                      'department': i, 'time': k.availabletime, 'fee': k.fee, 'isShow': False}
                            appDicList.append(appDic)

    return  appDicList;

def findAppByUser(name):
    patientList=list(models.Patient.objects.filter(name=name))
    appDicList=[]
    for i in patientList:
        appointmentsList=models.Appointment.objects.filter(id_patient=i.id_patient).filter(registrationtime__isnull=True)
        for j in appointmentsList :
            appDic={'anAppointment':j,'patient':j.id_patient,'bulletin':j.id_bulletin}
            appDicList.append(appDic)
    return appDicList;

def addUser(form):
    data = form.cleaned_data
    receptor = models.Adminreceptor.objects.create(loginname=data['username'], password=data['password'],
                                            createtime=datetime.datetime.now(), id_hospital=data['hospital'])
    receptor.save()
