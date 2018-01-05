from django.conf.urls import url
from . import views


urlpatterns = [url(r'^$', views.list_post, name='post_list'),
               url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',
                   views.post_detail, name='post_detail'),
               url(r'^add_post/$', views.add_post, name='add_post'),
               url(r'^edit_post/(?P<pk>\d+)/$',
                   views.edit, name='edit_post'),
               url(r'^delete_post/(?P<pk>\d+)/$',
                   views.delete, name='delete_post'),
]