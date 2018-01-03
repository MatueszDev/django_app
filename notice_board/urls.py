from django.conf.urls import url
from . import views


urlpatterns = [url(r'^$', views.add_post, name='post_list'),
               url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',
                   views.post_detail, name='post_detail'),
]