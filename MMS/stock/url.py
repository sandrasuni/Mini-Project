from django.conf.urls import url
from stock import views

urlpatterns = [
    url('stock/', views.stock),
    url('mansto/',views.mansto),
    url('update/(?P<stock_id>\w+)',views.update_stock,name='su'),
    url('delete/(?P<stock_id>\w+)',views.delete,name='sd'),
    url('purchase_list/',views.purchase_list)
]
