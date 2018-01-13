from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^ocr_scan/$', views.ocr_scan, name='ocr_scan'),
    url(r'^ocr_crop/$', views.ocr_crop, name='ocr_crop'),
]
