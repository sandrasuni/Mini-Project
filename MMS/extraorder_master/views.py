from django.shortcuts import render
from extraorder_master.models import ExtraorderMaster
from extraorder_sub.models import ExtraorderSub
from student.models import Student
from stock.models import Stock
from django.http import JsonResponse
from billing.models import MessBill
from mess_amount.models import MessAmount  # Adjust this import based on your app structure
from django.db.models import Sum
from django.utils import timezone
import calendar
from datetime import datetime
from datetime import datetime, timedelta
from django.db.models import Sum
from datetime import datetime, timedelta

def add_extra_order(request):
    item_name = ''
    price = 0
    student_name = ''
    total_price = 0
    mess_no = ''
    item_code = ''
    order_date = ''
    quantity = ''
    monthly_data = []  # List to hold data for each day of the month

    # Prepare student names and item details
    student_names = {str(student.mess_id): student.name for student in Student.objects.all()}
    item_details = {stock.item_code: {'name': stock.item_name, 'price': stock.price} for stock in Stock.objects.all()}

    # Handle form submission
    if request.method == 'POST':
        mess_no = request.POST.get('mess_no', '').strip()
        item_code = request.POST.get('item_code', '').strip()
        order_date = request.POST.get('order_date', '').strip()
        quantity = request.POST.get('quantity', '').strip()

        # Validate inputs
        if not mess_no or not item_code or not order_date or not quantity:
            error_message = "All fields are required."
            return render(request, 'extraorder_master/extraorder.html', {
                'error': error_message,
                'student_names': student_names,
                'item_details': item_details,
                'mess_no': mess_no,
                'item_code': item_code,
                'order_date': order_date,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Check if mess_no is a valid number
        if not mess_no.isdigit():
            error_message = "Invalid mess number. Please enter a valid number."
            return render(request, 'extraorder_master/extraorder.html', {
                'error': error_message,
                'student_names': student_names,
                'item_details': item_details,
                'mess_no': mess_no,
                'item_code': item_code,
                'order_date': order_date,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Convert mess_no to an integer for queries
        mess_no = int(mess_no)

        # Fetch student name based on mess number
        student = Student.objects.filter(mess_id=mess_no).first()
        if student:
            student_name = student.name  # Fetch the student's name
        else:
            return render(request, 'extraorder_master/extraorder.html', {
                'error': "No student found for this mess number.",
                'student_names': student_names,
                'item_details': item_details,
                'mess_no': mess_no,
                'item_code': item_code,
                'order_date': order_date,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Check if the student is on leave for the given date
        order_date_obj = datetime.strptime(order_date, '%Y-%m-%d').date()
        leave = LeaveRequest.objects.filter(
            mess=student,
            status='approved',  # Assuming 'status' is the field that indicates if leave is approved
            from_date__lte=order_date_obj,
            to_date__gte=order_date_obj
        ).first()

        if leave:
            return render(request, 'extraorder_master/extraorder.html', {
                'error': "Cannot place order: Student is on leave.",
                'student_names': student_names,
                'item_details': item_details,
                'mess_no': mess_no,
                'item_code': item_code,
                'order_date': order_date,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Fetch item details based on item code
        stock_item = Stock.objects.filter(item_code=item_code).first()
        if stock_item:
            item_name = stock_item.item_name
            price = stock_item.price
        else:
            return render(request, 'extraorder_master/extraorder.html', {
                'error': "No item found with this code.",
                'student_names': student_names,
                'item_details': item_details,
                'mess_no': mess_no,
                'item_code': item_code,
                'order_date': order_date,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Calculate total price
        if quantity.isdigit() and int(quantity) > 0:
            quantity = int(quantity)
            total_price = price * quantity
        else:
            return render(request, 'extraorder_master/extraorder.html', {
                'error': "Quantity must be a positive integer.",
                'student_names': student_names,
                'item_details': item_details,
                'mess_no': mess_no,
                'item_code': item_code,
                'order_date': order_date,
                'quantity': quantity,
                'total_price': total_price,
            })

        # Save the order if everything is valid
        master_order = ExtraorderMaster.objects.create(
            mess=student,
            item_name=item_name,
            order_date=order_date,
            total_price=total_price
        )
        ExtraorderSub.objects.create(
            order=master_order,
            stock=stock_item,
            price=price,
            quantity=quantity
        )

        # Reset the form after successful submission
        return render(request, 'extraorder_master/extraorder.html', {
            'success_message': "Extra order added successfully!",
            'student_names': student_names,
            'item_details': item_details,
            'mess_no': '',
            'item_code': '',
            'order_date': '',
            'quantity': '',
            'total_price': 0,
            'monthly_data': monthly_data,  # Pass the monthly data to the template
        })

    # Fetch monthly data based on the order date for the current month
    if order_date:
        order_date_obj = datetime.strptime(order_date, '%Y-%m-%d')
        first_day = order_date_obj.replace(day=1)
        last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        for single_date in (first_day + timedelta(n) for n in range((last_day - first_day).days + 1)):
            # Calculate mess amount
            mess_amount = ExtraorderMaster.objects.filter(
                order_date=single_date,
                mess__mess_id=mess_no  # assuming 'mess_id' is the field for the mess number
            ).aggregate(Sum('total_price'))['total_price__sum'] or 0

            # Calculate extra amount
            extra_amount = ExtraorderSub.objects.filter(
                order__order_date=single_date,
                order__mess__mess_id=mess_no
            ).aggregate(Sum('price'))['price__sum'] or 0

            total_amount = mess_amount + extra_amount

            monthly_data.append({
                'date': single_date.date(),
                'mess_amount': mess_amount,
                'extra_amount': extra_amount,
                'total_amount': total_amount,
            })

    return render(request, 'extraorder_master/extraorder.html', {
        'item_name': item_name,
        'price': price,
        'student_name': student_name,
        'total_price': total_price,
        'mess_no': mess_no,
        'item_code': item_code,
        'order_date': order_date,
        'quantity': quantity,
        'student_names': student_names,
        'item_details': item_details,
        'monthly_data': monthly_data,  # Pass the monthly data to the template
    })





# def add_extra_order(request):
#     item_name = ''
#     price = 0
#     student_name = ''
#     total_price = 0
#     mess_no = ''
#     item_code = ''
#     order_date = ''
#     quantity = ''

#     # Prepare student names and item details
#     student_names = {str(student.mess_id): student.name for student in Student.objects.all()}
#     item_details = {stock.item_code: {'name': stock.item_name, 'price': stock.price} for stock in Stock.objects.all()}

#     # Handle form submission
#     if request.method == 'POST':
#         mess_no = request.POST.get('mess_no', '')
#         item_code = request.POST.get('item_code', '')
#         order_date = request.POST.get('order_date', '')
#         quantity = request.POST.get('quantity', '')

#         # Fetch student name based on mess number
#         if mess_no:
#             student = Student.objects.filter(mess_id=mess_no).first()
#             if student:
#                 student_name = student.name  # Fetch the student's name

#         # Fetch item details based on item code
#         if item_code:
#             stock_item = Stock.objects.filter(item_code=item_code).first()
#             if stock_item:
#                 item_name = stock_item.item_name
#                 price = stock_item.price

#         # Calculate total price
#         if quantity and quantity.isdigit():
#             quantity = int(quantity)
#             total_price = price * quantity

#         # If everything is valid, save the order
#         if order_date and total_price and student_name:
#             master_order = ExtraorderMaster.objects.create(
#                 mess=student,
#                 item_name=item_name,
#                 order_date=order_date,
#                 total_price=total_price
#             )
#             ExtraorderSub.objects.create(
#                 order=master_order,
#                 stock=stock_item,
#                 price=price,
#                 quantity=quantity
#             )
#             return render(request, 'extraorder_master/extraorder.html', {
#                 'student_names': student_names,
#                 'item_details': item_details,
#                 'mess_no': '',
#                 'item_code': '',
#                 'order_date': '',
#                 'quantity': '',
#                 'total_price': 0,
#             })

#     return render(request, 'extraorder_master/extraorder.html', {
#         'item_name': item_name,
#         'price': price,
#         'student_name': student_name,
#         'total_price': total_price,
#         'mess_no': mess_no,
#         'item_code': item_code,
#         'order_date': order_date,
#         'quantity': quantity,
#         'student_names': student_names,
#         'item_details': item_details,
#     })


def fetch_student_name(request):
    mess_no = request.GET.get('mess_no', '').strip()  # Get the mess number from the request
    if not mess_no:
        return JsonResponse({'student_name': ''})  # Return an empty response if mess_no is not provided

    # Fetch the first student associated with the given mess number
    student = Student.objects.filter(mess_id=mess_no).first()
    # Return the student's name if found, otherwise return an empty string
    return JsonResponse({'student_name': student.name if student else ''})

def fetch_item_details(request):
    item_code = request.GET.get('item_code', '').strip()  # Get the item code from the request
    if not item_code:
        return JsonResponse({'item_name': '', 'price': 0})  # Return empty if item_code is not provided

    # Fetch the first stock item associated with the given item code
    item = Stock.objects.filter(item_code=item_code).first()
    # Return the item's name and price if found, otherwise return empty values
    if item:
        return JsonResponse({'item_name': item.item_name, 'price': item.price})
    return JsonResponse({'item_name': '', 'price': 0})  # Return empty if no item found



from django.db.models import Q
from datetime import datetime, timedelta
from mess_amount.models import MessAmount

from leave_request.models import LeaveRequest

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

def view_extra_orders(request):
    # Get the current month and year
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Fetch all extra orders for the current month
    extra_orders = ExtraorderMaster.objects.filter(order_date__month=current_month, order_date__year=current_year)

    # Fetch student names for the dropdown
    student_names = {str(student.mess_id): student.name for student in Student.objects.all()}

    # Handle search functionality
    mess_id = request.GET.get('mess_id', '').strip()

    # Filter extra orders based on mess_id input
    if mess_id:
        extra_orders = extra_orders.filter(mess__mess_id=mess_id)

    # Prepare monthly data for the calendar view
    month_dates = [
        today.replace(day=day).date() for day in range(1, (today.replace(month=(current_month % 12) + 1, day=1) - timedelta(days=1)).day + 1)
    ]

    # Fetch the daily mess amount
    daily_mess_amount = MessAmount.objects.first()
    daily_amount = daily_mess_amount.daily_amount if daily_mess_amount else 0

    # Initialize leave dates set
    leave_dates = set()

    # Retrieve leave requests for the student if `mess_id` is provided
    if mess_id:
        leave_requests = LeaveRequest.objects.filter(
            mess_id=mess_id,
            status='approved'
        )
        
        # Collect leave dates for all relevant leave requests
        for leave in leave_requests:
            # Create a range of dates for each leave request
            current_date = leave.from_date
            while current_date <= leave.to_date:
                leave_dates.add(current_date)
                current_date += timedelta(days=1)

    # Prepare dictionaries to store extra amounts and daily mess amounts based on filtered orders
    extra_amounts = {date: 0 for date in month_dates}
    daily_amounts = {}

    # Calculate daily amounts, ensuring leave days show as 0
    for date in month_dates:
        daily_amounts[date] = 0 if date in leave_dates else daily_amount

    # Populate extra amounts for the filtered orders
    for order in extra_orders:
        order_date = order.order_date  # Directly use order_date if it's already a date type
        if order_date in extra_amounts:
            extra_amounts[order_date] += order.total_price

    # Prepare a dictionary to store total prices (daily + extra amounts) for the filtered orders
    total_prices = {date: daily_amounts[date] + extra_amounts[date] for date in month_dates}

    # Calculate final total amount for the month
    total_mess_amount = sum(daily_amounts[date] for date in month_dates)  # Sum daily amounts
    total_extra_amount = sum(extra_amounts.values())  # Total extra amount for the month
    final_total_amount = total_mess_amount + total_extra_amount  # Total amount to pay for the month

    context = {
        'extra_orders': extra_orders,
        'month_dates': month_dates,
        'student_names': student_names,
        'current_month': current_month,
        'current_year': current_year,
        'mess_id': mess_id,
        'daily_amount': daily_amount,
        'daily_amounts': daily_amounts,
        'extra_amounts': extra_amounts,
        'total_prices': total_prices,
        'final_total_amount': final_total_amount,
    }

    return render(request, 'extraorder_master/view_extraorder.html', context)
