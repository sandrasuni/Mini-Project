from django.shortcuts import render
# from student.models import Student
from billing.models import MessBill
from mess_amount.models import MessAmount
from student.models import Student
from leave_request.models import LeaveRequest
from django.db.models import Q
# Create your views here.

# def vbill(request):
#     obj=MessBill.objects.all()
#     context={
#         'dd':obj
#     }
#     return render(request,'billing/billing.html',context)

# views.py

# views.py


# def mesb(request):
#     # Fetch all the mess amounts and students
#     mess_amounts = MessAmount.objects.all()
#     students = Student.objects.all()

#     # Create a context to pass data to the template
#     context = {
#         'mess_amounts': mess_amounts,
#         'students': students
#     }

#     return render(request, 'billing/billing.html', context)

from django.shortcuts import render
from billing.models import MessBill
from mess_amount.models import MessAmount
from student.models import Student
from django.utils import timezone

def mesb(request):
    # Fetch all the mess amounts and students
    mess_amounts = MessAmount.objects.all()
    students = Student.objects.all()

    # Create a context to pass data to the template
    context = {
        'mess_amounts': mess_amounts,
        'students': students
    }

    if request.method == 'POST':
        # Assuming you want to store bills when a form is submitted
        extra = request.POST.get('extra_amount', 0)  # Get extra amount from form input, default to 0 if not provided

        for student in students:
            if mess_amounts.exists():  # Ensure there's at least one mess amount
                daily_amount = mess_amounts.first().daily_amount  # Get the first daily amount

                # Create and populate a new MessBill instance
                obk = MessBill()
                obk.month = "2024-09-23"  # Set the month
                obk.year = "2024-09-23"  # Set the year
                obk.mess_id = student.mess_id
                obk.student_name = student.name
                obk.mess_amount = daily_amount  # Use the daily amount
                obk.extra_amount = extra  # Use the extra amount
                obk.total_amount = daily_amount + int(extra)  # Calculate total amount
                obk.save()  # Save the bill to the database

        # Optionally, you can redirect to a success page or show a message
        return render(request, 'billing/billing.html', context)

    return render(request, 'billing/billing.html', context)

from django.http import HttpResponse
from .models import MessBill  # Assuming you have a model for bills

from django.shortcuts import render
from .models import MessBill
from collections import defaultdict

def mess_bill_view(request):
    search_query = request.POST.get('search', '')
    selected_month = request.POST.get('month', '')
    selected_year = request.POST.get('year', '')

    # Get all years for the dropdown
    years = MessBill.objects.values_list('date__year', flat=True).distinct().order_by('date__year')

    # Filter bills based on the selected month and year
    bills = MessBill.objects.all()

    if selected_month and selected_year:
        bills = bills.filter(date__month=selected_month, date__year=selected_year)

    # If there's a search query, filter further
    if search_query:
        bills = bills.filter(mess_no__icontains=search_query) | bills.filter(student_name__icontains=search_query)

    # Organize bills by date
    bills_by_date = defaultdict(list)
    for bill in bills:
        bills_by_date[bill.date.day].append(bill)

    # Prepare data for the template
    context = {
        'search_query': search_query,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'years': years,
        'bills_by_date': bills_by_date,
    }

    return render(request, 'billing/vstu_bill.html', context)
