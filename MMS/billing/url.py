from django.conf.urls import url
from billing import views

urlpatterns=[
    url('billing/',views.view_messbill, name='view_messbill'),
    url('vstubill/',views.vstubill, name='vstubill'),
    url('indv/',views.indv_bill, name='indv'),
 ]