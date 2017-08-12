from django.conf.urls import url
import views

urlpatterns = [
    url('^$',views.index),
    url('^list/$', views.list),
    url('^detail/$', views.detail),
    url('^search/$', views.MySearchView.as_view()),
]