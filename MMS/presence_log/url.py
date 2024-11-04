from django.conf.urls import url
from presence_log import views


urlpatterns = [
    url('presence_log/', views.presence),
    url('fetch_student_details/', views.fetch_student_details, name='fetch_student_details'),  # Endpoint to fetch student details
] 