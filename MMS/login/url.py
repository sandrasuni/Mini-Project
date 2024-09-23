from django.urls import path
from login import views

urlpatterns = [
    #path('', views.login_view, name='homepage'),
    path('login/', views.login, name='login'),
]
