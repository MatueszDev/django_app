from django.conf.urls import url
from .import views
from grades.views import people

urlpatterns = [
    url(r'^$', views.choose_group, name='choose_field')
]
