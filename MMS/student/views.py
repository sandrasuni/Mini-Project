from django.shortcuts import render
from student.models import Student
from login.models import Login
from datetime import datetime
from django.utils import timezone
from django.views.decorators.cache import never_cache

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
    query_name = request.GET.get('student_name', '')  # Get the student name from the request
    query_mess_no = request.GET.get('mess_no', '')    # Get the mess number from the request
    
    # Filter students based on the search inputs
    students = Student.objects.all()
    
    if query_name:
        students = students.filter(name__icontains=query_name)  # Case-insensitive name filter

    if query_mess_no:
        students = students.filter(mess_id__icontains=query_mess_no)  # Case-insensitive mess_id filter
    
    total_students = Student.objects.count()  # Get the total count of all registered students

    context = {
        'dd': students,           # Passing filtered or all student data
        'total_students': total_students,  # Total count of students
    }
    return render(request, 'student/manage student.html', context)


from django.shortcuts import render, redirect
from django.utils import timezone

def update(request, idd):
    # Fetch the student object based on the 'mess_id'
    obb = Student.objects.get(mess_id=idd)

    # Get the current date for comparison or to disable past dates in the form
    now = timezone.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        # Update the student object with the form data
        obb.name = request.POST.get('ne')
        obb.joining_date = request.POST.get('date')
        obb.department = request.POST.get('d')

        # Save the updated student object
        obb.save()

        # Redirect to prevent the form from showing old values
        return ms(request)

    # Always retrieve the latest object data from the database to ensure form reflects the updated values
    updated_student = Student.objects.get(mess_id=idd)

    # Prepare the context with the latest student data
    context = {
        'dd': updated_student,
        'dt': now,  # Pass the current date to the template
    }
    
    # Render the form with the updated data
    return render(request, 'student/update.html', context)


# def update(request,idd):
    
#     obb = Student.objects.get(mess_id=idd)
#     now = datetime.now()
#     date_time = now.strftime("%Y-%m-%d")
#     context = {
#     'c':obb,
#     'dd':obb,
#     'dt':date_time,
#     } 

#     if request.method=="POST":
#         obj=Student.objects.get(mess_id=idd)
#         obj.name=request.POST.get('ne')
#         obj.joining_date=request.POST.get('date')
#         obj.department=request.POST.get('d')
        
#         obj.save()
#         return ms(request)
#     return render(request,'student/update.html',context)

def delete(request,idd):
    obj=Student.objects.get(mess_id=idd)
    obj.delete()
    return ms(request)

def vstud(request):
    obj=Student.objects.all()
    context={
        'dd':obj
    }



