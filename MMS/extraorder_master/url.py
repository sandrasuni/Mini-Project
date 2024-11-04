from django.conf.urls import url
from extraorder_master import views

urlpatterns=[
    url('add-extra-order/', views.add_extra_order, name='add_extra_order'),
    url('fetch-student-name/', views.fetch_student_name, name='fetch_student_name'),
    url('fetch-item-details/', views.fetch_item_details, name='fetch_item_details'),
    url('view-extra-orders/', views.view_extra_orders, name='view_extra_orders'),
    # url('fetch_mess_bill/', views.fetch_mess_bill, name='fetch_mess_bill'),
]
   

