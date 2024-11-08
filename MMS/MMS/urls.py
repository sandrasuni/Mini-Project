"""
URL configuration for MMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from Temp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url('login/',include('login.url')),
    url('student/', include('student.url')),
    url('billing/', include('billing.url')),
    url('menu_item/', include('menu_item.url')),
    url('stock/', include('stock.url')),
    url('presence_log/', include('presence_log.url')),
    url('mess_amount/', include('mess_amount.url')),
    url('leave_request/', include('leave_request.url')),
    url('extraorder_master/', include('extraorder_master.url')),
    url('report/', include('report.url')),
    url('Temp/',include('Temp.url')),
    url('$',views.home)
]