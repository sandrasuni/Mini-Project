from django.http import HttpResponseRedirect
from django.shortcuts import render
from login.models import Login
# Create your views here.
def login(request):
    if request.method == "POST":
        objlist=''
        uname = request.POST.get("user")
        passw = request.POST.get("password")
        obj =  Login.objects.filter(username=uname, password=passw)
        tp = ""
        for ob in obj:
            tp = ob.type
            uid = ob.uid
            if tp == "admin":
                request.session["uid"] = uid
                return HttpResponseRedirect('/Temp/admin/')
            elif tp =="student":
                request.session["uid"] = uid
                return HttpResponseRedirect('/Temp/user/')
        else:
            objlist = "username or password incorrect... Please try again..!"
            context ={
                'msg' :objlist,
            }
            return render(request,'login/login.html',context)
    return render(request,'login/login.html')



# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from login.models import Login

# def login(request):
#     if request.method == "POST":
#         uname = request.POST.get("user")
#         passw = request.POST.get("password")
#         obj = Login.objects.filter(username=uname, password=passw)

#         if obj.exists():
#             for ob in obj:
#                 tp = ob.type
#                 uid = ob.uid
#                 request.session["uid"] = uid
#                 if tp == "admin":
#                     return HttpResponseRedirect('/Temp/admin/')
#                 elif tp == "student":
#                     return HttpResponseRedirect('/Temp/user/')
#         else:
#             # This block will execute if no matching user is found
#             msg = "Username or password incorrect...Please try again..!"
#             context = {
#                 'msg': msg,
#             }
#             return render(request, 'login/login.html', context)

#     # If the request method is not POST, or if no error occurs
#     return render(request, 'login/login.html')


