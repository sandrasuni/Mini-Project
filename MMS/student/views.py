from django.shortcuts import render
from student.models import Student
from login.models import Login
from datetime import datetime
from django.utils import timezone
# Create your views here.

def student(request):
    date_time = timezone.now().strftime("%Y-%m-%d")
    obk=""
    if request.method=="POST":
        obj=Student()
        obj.name=request.POST.get('name')
        obj.joining_date=request.POST.get('date')
        obj.department=request.POST.get('department')
        
        #obj.password=request.POST.get('password')
        obj.save()
        context = {
             'dt': date_time
    }

        ob = Login()
        ob.username = obj.mess_id
        ob.password = request.POST.get('password')
        #ob.password = obj.password
        ob.type = 'student'
        ob.uid = obj.mess_id
        ob.save()
        obk = "successfully registered"
    context = {
            'msg': obk
    }
    return render(request,'student/student.html',context)


def ms(request):
    obj=Student.objects.all()
    context={
        'dd':obj
    }
    return render(request,'student/manage student.html',context)

def update(request,idd):
    
    obb = Student.objects.get(mess_id=idd)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    context = {
    'c':obb,
    'dd':obb,
    'dt':date_time,
    } 

    if request.method=="POST":
        obj=Student.objects.get(mess_id=idd)
        obj.name=request.POST.get('ne')
        obj.joining_date=request.POST.get('date')
        obj.department=request.POST.get('d')
        
        obj.save()
        return ms(request)
    return render(request,'student/update.html',context)

def delete(request,idd):
    obj=Student.objects.get(mess_id=idd)
    obj.delete()
    return ms(request)

def vstud(request):
    obj=Student.objects.all()
    context={
        'dd':obj
    }



