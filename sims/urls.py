# coding=utf-8

from django.conf.urls import url
from . import views

app_name = "sims"

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^upload/$', views.upload, name = 'upload'),
    url(r'^add/$', views.add),
    url(r'^edit/$', views.edit),
    url(r'^delete/$', views.delete),
    url(r'^write/$', views.write)
]
