from django.conf.urls import url
from Temp import views

urlpatterns=[
    url('home/',views.home),
    url('admin/',views.admin),
    url('log/',views.login),
    url('user/',views.user),
]