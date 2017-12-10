from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dev_fileview/$', views.dev_fileview, name='dev_fileview'),
    url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^add_text/$', views.add_text, name='add_text'),
    url(r'^add_pdf/$', views.add_pdf, name='add_pdf'),
    url(r'^dev_imgview/$', views.dev_imgview, name='dev_imgview'),
    url(r'^dev_pdfview/$', views.dev_pdfview, name='dev_pdfview'),
]
