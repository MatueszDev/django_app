from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dev_fileview/$', views.dev_fileview, name='dev_fileview')
]
