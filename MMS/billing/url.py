from django.conf.urls import url
from billing import views

urlpatterns=[
    url('billing/',views.mesb),
    url('vstubill/',views.mess_bill_view),
 ]