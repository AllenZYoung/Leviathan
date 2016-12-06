from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^hospital/$', views.hospital, name='hospital'),
    url(r'^department/$', views.department, name='department'),
    url(r'^test/$', views.test, name='test'),
    url(r'^doctor/$', views.doctor, name='doctor'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^usercenter/$', views.user_center, name='usercenter'),
    url(r'^usercenter/changeinfo/$', views.change_info, name='changeinfo'),
    url(r'^usercenter/accountsafe/$', views.change_pw, name='accountsafe'),
    url(r'^usercenter/viewa/$', views.view_appointment, name='viewa'),
    url(r'^pay/$',views.pay,name='pay'),
    url(r'^evaluate/$',views.evaluate,name='evaluate'),
]
