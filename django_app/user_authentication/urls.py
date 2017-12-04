from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'user_authentication/login_user.html'}),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'user_authentication/log_out.html'}),
    url(r'^register/', register),
]