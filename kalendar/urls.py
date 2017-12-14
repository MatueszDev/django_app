from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index' ),
    url(r'^addEvent/$', views.add_event, name='add_event'),
    #url(r'^(?P<info>\w+)/$', views.index, name='index_with_arg' ),
    url(r'^modifyEvent/(?P<object_id>\d+)/$', views.modify_event, name='modify_event'),
    url(r'^delete/(?P<object_id>\d+)/$', views.delete_event, name="deletion"),
    url(r'^allEventList', views.all_event_list, name="all_event_list"),
]