from django.shortcuts import render
from mess_amount.models import MessAmount
from student.models import Student
from leave_request.models import LeaveRequest
from django.db.models import Q
from extraorder_master.models import ExtraorderMaster # Import the Student model if needed
from django.db.models import Sum
from django.utils.timezone import now
import calendar
from datetime import timedelta
from django.db.models import Q


def view_messbill(request):
    # Get month and year from GET parameters or use the current month/year
    current_month = int(request.GET.get('month', timezone.now().month))
    current_year = int(request.GET.get('year', timezone.now().year))

    # Month names
    month_names = list(calendar.month_name)[1:]  # Skip the first empty entry

    # Calculate the number of days in the current month
    days_in_month = calendar.monthrange(current_year, current_month)[1]

    # Fetch all students
    student_data = Student.objects.all()

    # Initialize bill data and grand total
    bill_data = []
    grand_total = 0

    for student in student_data:
        # Check if the student joined before the selected month/year
        if student.joining_date.year < current_year or (student.joining_date.year == current_year and student.joining_date.month <= current_month):
            # Fetch the daily amount for mess charges
            daily_amount = MessAmount.objects.values_list('daily_amount', flat=True).first() or 0

            # Fetch approved leave requests in the current month
            leave_requests = LeaveRequest.objects.filter(
                mess_id=student.mess_id,
                status='approved'
            ).filter(
                Q(from_date__month=current_month, from_date__year=current_year) |
                Q(to_date__month=current_month, to_date__year=current_year) |
                Q(from_date__lt=timezone.datetime(current_year, current_month, days_in_month, 23, 59, 59),
                  to_date__gt=timezone.datetime(current_year, current_month, 1))
            )

            # Use a set to collect unique leave dates
            leave_dates = set()

            # Loop through each leave request and add dates to the set
            for leave in leave_requests:
                current_date = leave.from_date
                while current_date <= leave.to_date:
                    if current_date.month == current_month and current_date.year == current_year:
                        leave_dates.add(current_date)
                    current_date += timedelta(days=1)

            # Count unique leave days
            approved_leave_days = len(leave_dates)

            # Calculate the effective amount considering leave days
            effective_days = days_in_month - approved_leave_days
            effective_daily_amount = daily_amount * effective_days

            # Sum extra orders for the given month and year for each student
            extra_orders_total = ExtraorderMaster.objects.filter(
                mess_id=student.mess_id,
                order_date__month=current_month,
                order_date__year=current_year
            ).aggregate(total_extra_amount=Sum('total_price'))['total_extra_amount'] or 0

            # Calculate the total amount for the month
            total_amount = effective_daily_amount + extra_orders_total

            # Append the data
            bill_data.append({
                'mess_no': student.mess_id,
                'student_name': student.name,
                'total_amount': total_amount,
                'approved_leave_days': approved_leave_days,  # Include leave days for debugging
            })

            # Add to grand total
            grand_total += total_amount

    # Check if bill_data is empty and set a message accordingly
    no_data_message = ""
    if not bill_data:
        no_data_message = "No data available for this year or month."

    # Create a list of years from 2020 to the current year
    year_range = list(range(2020, timezone.now().year + 1))

    # Render the template with context
    return render(request, 'billing/billing.html', {
        'dd': bill_data,
        'no_data_message': no_data_message,
        'current_month': current_month,
        'current_year': current_year,
        'month_names': month_names,  # Pass the month names to the template
        'year_range': year_range,     # Pass the year range to the template
        'total_amount_sum': grand_total,  # Pass the grand total to the template
    })



from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Sum
import calendar

def vstubill(request):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Get the selected month and year from the request, with defaults to current month/year
    month = int(request.GET.get('month', current_month))
    year = int(request.GET.get('year', current_year))

    # Choices for month and year dropdowns
    month_choices = {i: calendar.month_name[i] for i in range(1, 13)}
    year_choices = list(range(2020, current_year + 1))

    # Filter students who joined on or before the selected month and year
    registered_students = Student.objects.filter(
        Q(joining_date__year__lt=year) | 
        (Q(joining_date__year=year) & Q(joining_date__month__lte=month))
    )

    if not registered_students.exists():
        context = {
            'no_bill_message': f'No bill available for selected month: {calendar.month_name[month]} {year}.',
            'student_names': {},
            'current_month': month,
            'current_year': year,
            'mess_id': request.GET.get('mess_id', '').strip(),
            'monthly_data': {},
            'month_choices': month_choices,
            'year_choices': year_choices,
        }
        return render(request, 'billing/vstu_bill.html', context)

    # Filter extra orders for the selected month and year
    extra_orders = ExtraorderMaster.objects.filter(
        order_date__year=year,
        order_date__month=month
    )

    # Create a dictionary of student names with mess IDs
    student_names = {str(student.mess_id): student.name for student in registered_students}
    mess_id = request.GET.get('mess_id', '').strip()
    if mess_id:
        extra_orders = extra_orders.filter(mess__mess_id=mess_id)

    # Get all dates in the selected month
    last_day = calendar.monthrange(year, month)[1]
    month_dates = [
        today.replace(year=year, month=month, day=day).date()
        for day in range(1, last_day + 1)
    ]

    # Retrieve the daily mess amount
    daily_mess_amount = MessAmount.objects.first()
    daily_amount = daily_mess_amount.daily_amount if daily_mess_amount else 0

    # Set up leave dates
    leave_dates = set()
    if mess_id:
        leave_requests = LeaveRequest.objects.filter(
            mess_id=mess_id,
            status='approved'
        ).filter(
            Q(from_date__year=year, from_date__month=month) |
            Q(to_date__year=year, to_date__month=month) |
            Q(from_date__lt=timezone.datetime(year, month, 1),
              to_date__gt=timezone.datetime(year, month, last_day))
        ).values('from_date', 'to_date')

        for leave in leave_requests:
            start_date = max(leave['from_date'], timezone.datetime(year, month, 1).date())
            end_date = min(leave['to_date'], timezone.datetime(year, month, last_day).date())
            
            leave_dates.update(
                [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            )

    # Calculate daily mess charges, adjusting for leave days
    daily_amounts = {date: (0 if date in leave_dates else daily_amount) for date in month_dates}

    # Calculate extra order amounts for each date in the month
    extra_order_totals = extra_orders.values('order_date').annotate(total_price=Sum('total_price'))
    extra_amounts = {date: 0 for date in month_dates}
    for order in extra_order_totals:
        order_date = order['order_date']
        if order_date in extra_amounts:
            extra_amounts[order_date] = order['total_price']

    # Calculate total prices for each day
    total_prices = {date: daily_amounts[date] + extra_amounts[date] for date in month_dates}

    # Overall totals
    total_mess_amount = daily_amount * (len(month_dates) - len(leave_dates))
    total_extra_amount = sum(extra_amounts.values())
    final_total_amount = total_mess_amount + total_extra_amount

    context = {
        'extra_orders': extra_orders,
        'month_dates': month_dates,
        'student_names': student_names,
        'current_month': month,
        'current_year': year,
        'mess_id': mess_id,
        'daily_amount': daily_amount,
        'daily_amounts': daily_amounts,
        'extra_amounts': extra_amounts,
        'total_prices': total_prices,
        'final_total_amount': final_total_amount,
        'month_choices': month_choices,
        'year_choices': year_choices,
    }

    # Add a message if there are no extra orders but registered students exist
    if not extra_orders.exists() and registered_students.exists():
        context['no_bill_message'] = f'No bill available for selected month: {calendar.month_name[month]} {year}.'

    return render(request, 'billing/vstu_bill.html', context)





from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
import calendar
from datetime import timedelta

from django.db.models import Q, Sum


def indv_bill(request):
    mess_id = request.session.get("uid")
    student_instance = Student.objects.get(mess_id=mess_id)

    # Get the current date dynamically to avoid stale data
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Use request parameters for month and year, falling back to the current values
    month = int(request.GET.get('month', current_month))
    year = int(request.GET.get('year', current_year))

    month_choices = {i: calendar.month_name[i] for i in range(1, 13)}
    year_choices = list(range(2020, current_year + 1))

    # Only show bills from the student's joining month onward
    joining_month = student_instance.joining_date.month
    joining_year = student_instance.joining_date.year

    if (year < joining_year) or (year == joining_year and month < joining_month):
        context = {
            'no_bill_message': f"Bills are available only from {calendar.month_name[joining_month]} {joining_year} onward.",
            'month_choices': month_choices,
            'year_choices': year_choices,
            'current_month': month,
            'current_year': year,
        }
        return render(request, 'billing/indv_bill.html', context)

    # Filter extra orders for the selected month and year
    extra_orders = ExtraorderMaster.objects.filter(
        order_date__year=year,
        order_date__month=month,
        mess=student_instance
    )

    # Generate a list of all dates in the month
    last_day = calendar.monthrange(year, month)[1]
    month_dates = [
        today.replace(year=year, month=month, day=day).date()
        for day in range(1, last_day + 1)
    ]

    daily_mess_amount = MessAmount.objects.first()
    daily_amount = daily_mess_amount.daily_amount if daily_mess_amount else 0

    # Leave dates
    leave_dates = set()
    leave_requests = LeaveRequest.objects.filter(
        mess_id=mess_id,
        status='approved'
    ).filter(
        Q(from_date__year=year, from_date__month=month) |
        Q(to_date__year=year, to_date__month=month) |
        Q(from_date__lt=timezone.datetime(year, month, 1),
          to_date__gt=timezone.datetime(year, month, last_day))
    ).values('from_date', 'to_date')

    for leave in leave_requests:
        start_date = max(leave['from_date'], timezone.datetime(year, month, 1).date())
        end_date = min(leave['to_date'], timezone.datetime(year, month, last_day).date())
        
        leave_dates.update(
            [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        )

    # Daily amounts, considering leave days
    daily_amounts = {date: (0 if date in leave_dates else daily_amount) for date in month_dates}

    # Calculate extra amounts for each day in the month
    extra_order_totals = extra_orders.values('order_date').annotate(total_price=Sum('total_price'))
    extra_amounts = {date: 0 for date in month_dates}
    for order in extra_order_totals:
        order_date = order['order_date']
        if order_date in extra_amounts:
            extra_amounts[order_date] = order['total_price']

    # Total prices for each day
    total_prices = {date: daily_amounts[date] + extra_amounts[date] for date in month_dates}

    # Overall totals
    total_mess_amount = daily_amount * (len(month_dates) - len(leave_dates))
    total_extra_amount = sum(extra_amounts.values())
    final_total_amount = total_mess_amount + total_extra_amount

    context = {
        'extra_orders': extra_orders,
        'month_dates': month_dates,
        'student_name': student_instance.name,
        'current_month': month,
        'current_year': year,
        'daily_amount': daily_amount,
        'daily_amounts': daily_amounts,
        'extra_amounts': extra_amounts,
        'total_prices': total_prices,
        'final_total_amount': final_total_amount,
        'month_choices': month_choices,
        'year_choices': year_choices,
    }

    if not extra_orders.exists():
        context['no_bill_message'] = f'No bill available for selected month: {calendar.month_name[month]} {year}.'

    return render(request, 'billing/indv_bill.html', context)
