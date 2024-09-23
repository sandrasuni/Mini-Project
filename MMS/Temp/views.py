from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'Temp/home.html')

def admin(request):
    return render(request,'Temp/admin.html')

def login(request):
    return render(request,'Temp/login.html')

def user(request):
    return render(request,'Temp/user.html')