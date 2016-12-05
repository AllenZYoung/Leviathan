from django.conf.urls import url
from receptor import views as recViews

urlpatterns = [
    url('^$',recViews.index),
    url('^login/$',recViews.login,name='login'),
    url('^logout/$',recViews.logout,name='logout'),
    url(r'^showAppointments/(\w+)*$',recViews.showAppoint,name='showAppointments'),
    url('^confirmAppointments/$',recViews.confirmAppointment,name='confirmAppointments'),
    url('^printAppointment/$',recViews.printAppointment,name='printAppointment'),
    url('^register/$',recViews.register,name='register'),
    url(r'^patient/(\w+)$',recViews.showPatient,name='patient'),

]