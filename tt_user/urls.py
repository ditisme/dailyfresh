from django.conf.urls import url
import views

urlpatterns = [
    url('^register/$', views.register),
    url('^register_handle/$', views.register_handle),
    url(r'^check_user_name/$', views.check_user_name),
    url('^login/$', views.login),
    url(r'^login_handle-/$', views.login_handle_nv),
    url('^login_handle/$', views.login_handle),
    url('^verify_code/$', views.verify_code),
    url('^logout/$', views.logout),
    url('^$', views.center),
    url('^order/$', views.order),
    url('^site/$', views.site),
    url('^islogin/$', views.islogin),
]