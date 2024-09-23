from django.shortcuts import render
from mess_amount.models import MessAmount
from django.http import HttpResponseRedirect

# Create your views here.

def mess_amount(request):
    obj = MessAmount.objects.first()
    context = {
        'd':obj,
    }
    if request.method=="POST":
        obj=MessAmount()
        obj.messamount_id=1
        obj.daily_amount=request.POST.get('mess_amount')        
        obj.save()
        # return HttpResponseRedirect('/billing/update/1')
    return render(request,'mess_amount/mess amount.html',context)

def mma(request):
    obj=MessAmount.objects.all()
    context={
        'dd':obj
    }
    return render(request,'mess_amount/manage messamount.html',context)

def messamount_update(request,idd):   
    obj = MessAmount.objects.get(messamount_id=idd)
    context = {
        'd':obj,
    }
    if request.method=="POST":
        obj=MessAmount.objects.get(messamount_id=idd)
        obj.messamount_id=1
        obj.daily_amount=request.POST.get('mess_amount')  
        obj.save()
        # return mma(request)
    return render(request,'mess_amount/messamount_update.html',context)