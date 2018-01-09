from django.conf.urls import url, include
from django.views.generic import  ListView, DetailView
from grades.models import Grades_group
from .import views

urlpatterns = [
    url(r'^$', views.choose_group, name='choose_field')
]
