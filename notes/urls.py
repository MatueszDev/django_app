from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.choose_class, name='choose_class'),
    url(r'^(?P<subject>[A-Za-z0-9]+)/(?P<lecture_number>[0-9]+)/$', views.select_lecture, name='select_lecture'),
    url(r'^add_note/$', views.add_note, name='add_note'),
    url(r'^add_file/$', views.add_file, name='add_file'),
#    url(r'^add_image/$', views.add_image, name='add_image'),
#    url(r'^add_text/$', views.add_text, name='add_text'),
#    url(r'^add_pdf/$', views.add_pdf, name='add_pdf'),
]
