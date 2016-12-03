from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^alter/(?P<bulletin_id>\d+)/$', views.alter_bulletin, name='alter'),
    url(r'^delete/(?P<bulletin_id>\d+)/$', views.delete_bulletin, name='delete'),
    url(r'^create/$', views.create_bulletin, name='create'),
    url(r'^batchUpload/$', views.batch_import_bulletin_by_excel, name='batchUpload'),

]