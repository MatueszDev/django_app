from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/add_ocr/$',
        views.add_ocr, name='add_ocr'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/add_crop/$',
        views.add_crop, name='add_crop'),
]
