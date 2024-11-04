from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render
from django.db.models import Sum
from stock.models import Stock
from mess_amount.models import MessAmount
from extraorder_master.models import ExtraorderMaster
from student.models import Student
from django.db.models import Sum, F  # Import F for field references
from leave_request.models import LeaveRequest
from datetime import datetime, timedelta

from django.db.models import Sum, F, Q
from datetime import datetime, timedelta, date

def profit_loss_report(request):
    # Get the current month and year, or default to the current date
    month = int(request.GET.get('month', datetime.now().month))
    year = int(request.GET.get('year', datetime.now().year))

    # Determine the first and last day of the selected month
    first_day_of_month = date(year, month, 1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Total days in the month
    total_days_in_month = (last_day_of_month - first_day_of_month).days + 1

    # Get daily amount for the current month
    daily_amount = MessAmount.objects.first()  # Assuming there's one daily amount applicable
    daily_amount_value = daily_amount.daily_amount if daily_amount else 0

    total_mess_income = 0

    # Calculate total income for each student
    for student in Student.objects.all():
        # Count leave days for this student within the selected month using unique dates
        leave_days_queryset = LeaveRequest.objects.filter(
            mess=student,
            status='approved',
            from_date__lte=last_day_of_month,
            to_date__gte=first_day_of_month
        )

        # Use a set to track unique leave dates within the month
        leave_dates = set()
        for leave in leave_days_queryset:
            current_date = leave.from_date
            while current_date <= leave.to_date:
                # Convert current_date to date if it's a datetime
                if isinstance(current_date, datetime):
                    current_date = current_date.date()
                if first_day_of_month <= current_date <= last_day_of_month:
                    leave_dates.add(current_date)
                current_date += timedelta(days=1)

        # Total unique leave days
        leave_days = len(leave_dates)

        # Ensure leave_days does not exceed total_days_in_month
        leave_days = min(leave_days, total_days_in_month)

        # Calculate income based on total days minus leave days
        total_income_for_student = (total_days_in_month - leave_days) * daily_amount_value
        total_mess_income += total_income_for_student

    # Calculate total extra orders income for the month
    total_extra_order_income = ExtraorderMaster.objects.filter(
        order_date__range=[first_day_of_month, last_day_of_month]
    ).aggregate(total_extra_order_value=Sum('total_price'))['total_extra_order_value'] or 0

    # Calculate total income including extra order income
    total_income = total_mess_income + total_extra_order_income

    # Calculate total stock expenses
    total_stock_expense = Stock.objects.aggregate(
        total_stock_value=Sum(F('stock_quantity') * F('price'))
    )['total_stock_value'] or 0

    # Total expense is the total stock expense; adjust as necessary
    total_expense = total_stock_expense  

    # Calculate profit or loss
    profit_or_loss = total_income - total_expense
    is_profit = profit_or_loss > 0

    # Prepare context for rendering
    context = {
        'total_income': total_income,  # Now includes both mess and extra order income
        'total_mess_income': total_mess_income,
        'total_extra_order_income': total_extra_order_income,
        'total_stock_expense': total_stock_expense,
        'total_expense': total_expense,
        'profit_or_loss': profit_or_loss,
        'is_profit': is_profit,
        'month': month,
        'years': [year for year in range(datetime.now().year - 5, datetime.now().year + 1)],  # Adjust year range as necessary
        'selected_year': year,
    }

    return render(request, 'report/report.html', context)

