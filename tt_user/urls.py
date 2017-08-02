from django.conf.urls import url
import views

urlpatterns = [
    url('^register/$', views.register),
    url('^register_handle/$', views.register_handle),
    url('^check_user_name_(\w+)/$', views.check_user_name),
    url('^login/$', views.login),
    url('^login_handle_(\w+)/$', views.login_handle_name),
    url('^login_handle_(\w+)-(.+)/$', views.login_handle_pwd),
    url('^login_handle/$', views.login_handle),
    url('^index/$', views.index),
]