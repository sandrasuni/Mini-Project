from django.conf.urls import url
from menu_item import views

urlpatterns = [
    url('menu/', views.menu, name='menu'),
    url('vm/', views.view_menu, name='vm'),
    url('manage/',views.manage, name='manage'),
    url('update/(?P<item_id>\w+)', views.update_item, name='aa'),
    url('delete/(?P<idd>\w+)',views.delete_item,name='bb')
]