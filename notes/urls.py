from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dev_fileview/$', views.dev_fileview, name='dev_fileview'),
    url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^add_text/$', views.add_text, name='add_text'),
]
