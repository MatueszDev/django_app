from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^get_drawings/$', views.get_drawings, name='get_drawings'),
    url(r'^show_cropped/$', views.show_cropped, name='show_cropped'),
]
