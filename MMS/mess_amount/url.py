from django.conf.urls import url
from mess_amount import views

urlpatterns=[
    url('messamount/',views.mess_amount),
    # url('mma/',views.mma),
    # url('update/(?P<idd>\w+)',views.messamount_update),

]