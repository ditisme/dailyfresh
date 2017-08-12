from django.conf.urls import url
import views
urlpatterns = [
    url('^add/$', views.add),
    url('^$', views.cart),
    url('^set_num/$', views.set_num),
    url('^delcart/$',views.delcart),
    url('^count/$', views.count),
]