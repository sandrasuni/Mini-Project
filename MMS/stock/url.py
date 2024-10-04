from django.conf.urls import url
from stock import views

urlpatterns = [
    url('stock/', views.stock),
    url('mansto/',views.mansto),
    url('update/(?P<stock_id>\w+)',views.update_stock,name='su'),
    url('delete/(?P<idd>\w+)',views.delete,name='sd'),
]
