from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
#    url('^scan$', views.scan, name='scan'),
    url(r'^add_image/$', views.add_image, name='add_image'),
]
