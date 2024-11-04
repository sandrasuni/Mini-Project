from django.conf.urls import url
from report import views

urlpatterns=[
    url('profit_loss_report/', views.profit_loss_report, name='profit_loss_report'),
]