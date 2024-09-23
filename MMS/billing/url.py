from django.conf.urls import url
from billing import views

urlpatterns=[
    url('billing/',views.mesb),
    # url('vstubill/',views.view_mess_bill),
 ]