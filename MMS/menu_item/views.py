from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from menu_item.models import Menu

# View for managing the menu

# def menu(request):
#     if request.method == "POST":
#         obj = Menu() 
#         obj.day = request.POST.get('day')
#         obj.menu_item = request.POST.get("item_name")
#         obj.menu_type = request.POST.get("menu_type")
        
#         price = request.POST.get('price', None) 
        
#         if not price:
#             price = 0 
#         else:
#             price = price 
        
#         obj.price = price
#         obj.save()

        
#     return render(request, 'menu_item/menu.html')


# def menu(request):
#     if request.method == "POST":
#         day = request.POST.get('day')

#         # Handle breakfast items
#         breakfast_items = request.POST.getlist('breakfast_items')
#         for item_name in breakfast_items:
#             if item_name:  # Ensure the item name is not empty
#                 obj = Menu(day=day, menu_item=item_name, menu_type='breakfast', price=0.0)
#                 obj.save()

#         # Handle lunch items
#         lunch_items = request.POST.getlist('lunch_items')
#         for item_name in lunch_items:
#             if item_name:
#                 obj = Menu(day=day, menu_item=item_name, menu_type='lunch', price=0.0)
#                 obj.save()

#         # Handle tea snack items
#         tea_snack_items = request.POST.getlist('tea_snack_items')
#         for item_name in tea_snack_items:
#             if item_name:
#                 obj = Menu(day=day, menu_item=item_name, menu_type='tea_snacks', price=0.0)
#                 obj.save()

#         # Handle dinner items
#         dinner_items = request.POST.getlist('dinner_items')
#         for item_name in dinner_items:
#             if item_name:
#                 obj = Menu(day=day, menu_item=item_name, menu_type='dinner', price=0.0)
#                 obj.save()

#         # Handle special items
#         special_item_name = request.POST.get('special_item_name')
#         price = request.POST.get('price', 0.0)
#         if special_item_name:
#             obj = Menu(day=day, menu_item=special_item_name, menu_type='special', price=float(price) if price else 0.0)
#             obj.save()

#         # Success message
#         messages.success(request, "Menu items added successfully!")
#         return redirect('menu')  # Redirect to prevent resubmission

#     selected_day = request.GET.get('day', '')  # Get the selected day from the request
#     if selected_day:
#         menu_items = Menu.objects.filter(day=selected_day)  # Filter menu items by selected day
#     else:
#         menu_items = Menu.objects.all()  # Get all menu items if no day is selected

#     # Prepare context data
#     context = {
#         'menu_items': menu_items,  # Pass menu items to the template
#         'selected_day': selected_day,  # Pass the selected day to the template
#     }

#     return render(request, 'menu_item/menu.html', context)

def menu(request):
    if request.method == "POST":
        day = request.POST.get('day')

        # Handle breakfast items
        breakfast_items = request.POST.getlist('breakfast_items')
        for item_name in breakfast_items:
            if item_name:  # Ensure the item name is not empty
                obj = Menu(day=day, menu_item=item_name, menu_type='breakfast', price=0.0)
                obj.save()

        # Handle lunch items
        lunch_items = request.POST.getlist('lunch_items')
        for item_name in lunch_items:
            if item_name:
                obj = Menu(day=day, menu_item=item_name, menu_type='lunch', price=0.0)
                obj.save()

        # Handle tea snack items
        tea_snack_items = request.POST.getlist('tea_snack_items')
        for item_name in tea_snack_items:
            if item_name:
                obj = Menu(day=day, menu_item=item_name, menu_type='tea_snacks', price=0.0)
                obj.save()

        # Handle dinner items
        dinner_items = request.POST.getlist('dinner_items')
        for item_name in dinner_items:
            if item_name:
                obj = Menu(day=day, menu_item=item_name, menu_type='dinner', price=0.0)
                obj.save()

        # Handle special items
        special_item_name = request.POST.get('special_item_name')
        price = request.POST.get('price', 0.0)
        if special_item_name:
            obj = Menu(day=day, menu_item=special_item_name, menu_type='special', price=float(price) if price else 0.0)
            obj.save()

        # Success message
        messages.success(request, "Menu items added successfully!")
        return redirect('menu')  # Redirect to prevent resubmission

    selected_day = request.GET.get('day', '')  # Get the selected day from the request
    if selected_day:
        menu_items = Menu.objects.filter(day=selected_day)  # Filter menu items by selected day
    else:
        menu_items = Menu.objects.all()  # Get all menu items if no day is selected

    # Prepare context data
    context = {
        'breakfast_items': menu_items.filter(menu_type='breakfast'),
        'lunch_items': menu_items.filter(menu_type='lunch'),
        'tea_snack_items': menu_items.filter(menu_type='tea_snacks'),
        'dinner_items': menu_items.filter(menu_type='dinner'),
        'special_items': menu_items.filter(menu_type='special'),
        'selected_day': selected_day,  # Pass the selected day to the template
    }

    return render(request, 'menu_item/menu.html', context)

# def update(request,idd):
    
#     obb = Menu.objects.get(menu_id=idd)
#     context = {
#     'c':obb,
#     'dd':obb,
#     } 

#     if request.method=="POST":
#         obb.day=request.POST.get('day')
#         obb.menu_item=request.POST.get('item_name')
#         obb.menu_type=request.POST.get('menu_type')
#         obb.price=request.POST.get('price')

#         obb.save()
#         return menu(request)
#     return render(request,'menu_item/update.html',context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Menu  # Ensure you import your Menu model

def update_item(request, item_id):
    # Fetch the menu item or return a 404 error if not found
    item = get_object_or_404(Menu, menu_id=item_id)

    if request.method == 'POST':
        # Get updated values from the form
        updated_item_name = request.POST.get('item_name')  # Use 'item_name' as per your form field
        updated_price = request.POST.get('price')  # Use 'price' as per your form field

        # Update item details
        item.menu_item = updated_item_name
        item.price = updated_price
        item.save()  # Save the updated item to the database

        # Display a success message and redirect to the manage page
        messages.success(request, 'Special item updated successfully!')
        return redirect('manage')  # Ensure 'manage' is the name of your manage view

    # If it's not a POST request, render the update page with existing item data
    return render(request, 'menu_item/update.html', {'item': item})



# Update item view
# def update_item(request, item_id):
#     item = get_object_or_404(Menu, id=item_id)
#     if request.method == 'POST':
#         updated_item_name = request.POST.get('updated_item')
#         item.menu_item = updated_item_name
#         item.save()
#         messages.success(request, 'Special item updated successfully!')
#         return redirect('manage')
#     return redirect('manage')

from django.shortcuts import render
from .models import Menu

# def manage(request):
#     if request.method == 'POST':
#         # Get form data
#         day = request.POST.get('day')
#         breakfast_item = request.POST.get('breakfast_items')
#         lunch_item = request.POST.get('lunch_items')
#         tea_snack_item = request.POST.get('tea_snack_items')
#         dinner_item = request.POST.get('dinner_items')
#         special_item_name = request.POST.get('special_item_name')
#         price = request.POST.get('price')

#         # Save data to the Menu model, ensuring consistent menu_type values
#         if breakfast_item:
#             Menu.objects.create(day=day, menu_type='Breakfast', menu_item=breakfast_item)
#         if lunch_item:
#             Menu.objects.create(day=day, menu_type='Lunch', menu_item=lunch_item)
#         if tea_snack_item:
#             Menu.objects.create(day=day, menu_type='Tea Snack', menu_item=tea_snack_item)
#         if dinner_item:
#             Menu.objects.create(day=day, menu_type='Dinner', menu_item=dinner_item)
#         if special_item_name and price:
#             Menu.objects.create(day=day, menu_type='Special', menu_item=special_item_name, price=price)

#         return redirect('manage')  # Redirect after form submission

#     # Handle GET request: Fetch the existing menu items
#     selected_day = request.GET.get('day', '')  # Get the selected day from the request
#     if selected_day:
#         # Filter items by selected day and menu type
#         menu_items = Menu.objects.filter(day=selected_day)
#     else:
#         # Default to all items if no day is selected
#         menu_items = Menu.objects.all()

#     # Prepare context data, ensuring correct filtering by menu_type
#     context = {
#         'breakfast_items': menu_items.filter(menu_type='Breakfast'),
#         'lunch_items': menu_items.filter(menu_type='Lunch'),
#         'tea_snack_items': menu_items.filter(menu_type='Tea Snack'),  # Ensure proper filtering
#         'dinner_items': menu_items.filter(menu_type='Dinner'),
#         'special_items': menu_items.filter(menu_type='Special'),
#         'selected_day': selected_day,  # Pass the selected day to the template
# }

#     return render(request, 'menu_item/manage.html', context)



def manage(request):
    if request.method == 'POST':
        # Get form data
        day = request.POST.get('day')
        breakfast_item = request.POST.get('breakfast_items')
        lunch_item = request.POST.get('lunch_items')
        tea_snack_item = request.POST.get('tea_snack_items')
        dinner_item = request.POST.get('dinner_items')
        special_item_name = request.POST.get('special_item_name')
        price = request.POST.get('price')

        # Save data to the Menu model
        if breakfast_item:
            Menu.objects.create(day=day, menu_type='Breakfast', menu_item=breakfast_item)
        if lunch_item:
            Menu.objects.create(day=day, menu_type='Lunch', menu_item=lunch_item)
        if tea_snack_item:
            Menu.objects.create(day=day, menu_type='Tea Snack', menu_item=tea_snack_item)
        if dinner_item:
            Menu.objects.create(day=day, menu_type='Dinner', menu_item=dinner_item)
        if special_item_name and price:
            Menu.objects.create(day=day, menu_type='Special', menu_item=special_item_name, price=price)

        return redirect('manage')  # Redirect after form submission

    # Handle GET request: Fetch the existing menu items
    selected_day = request.GET.get('day', '')  # Get the selected day from the request
    if selected_day:
        menu_items = Menu.objects.filter(day=selected_day)  # Filter menu items by selected day
    else:
        menu_items = Menu.objects.all()  # Get all menu items if no day is selected

    # Prepare context data
    context = {
        'breakfast_items': menu_items.filter(menu_type='breakfast'),
        'lunch_items': menu_items.filter(menu_type='lunch'),
        'tea_snack_items': menu_items.filter(menu_type='tea_snacks'),
        'dinner_items': menu_items.filter(menu_type='dinner'),
        'special_items': menu_items.filter(menu_type='special'),
        'selected_day': selected_day,  # Pass the selected day to the template
    }

    return render(request, 'menu_item/manage.html', context)

# def manage(request):
#     if request.method == 'POST':
#         # Get form data
#         day = request.POST.get('day')
#         breakfast_item = request.POST.get('breakfast_items')
#         lunch_item = request.POST.get('lunch_items')
#         tea_snack_item = request.POST.get('tea_snack_items')
#         dinner_item = request.POST.get('dinner_items')
#         special_item_name = request.POST.get('special_item_name')
#         price = request.POST.get('price')

#         # Save data to the Menu model
#         if breakfast_item:
#             Menu.objects.create(day=day, menu_type='Breakfast', menu_item=breakfast_item)
#         if lunch_item:
#             Menu.objects.create(day=day, menu_type='Lunch', menu_item=lunch_item)
#         if tea_snack_item:
#             Menu.objects.create(day=day, menu_type='Tea Snack', menu_item=tea_snack_item)
#         if dinner_item:
#             Menu.objects.create(day=day, menu_type='Dinner', menu_item=dinner_item)
#         if special_item_name and price:
#             Menu.objects.create(day=day, menu_type='Special', menu_item=special_item_name, price=price)

#         return redirect('manage')  # Redirect after form submission

#     # Handle GET request: Fetch the existing menu items
#     selected_day = request.GET.get('day', '')  # Get the selected day from the request
#     if selected_day:
#         menu_items = Menu.objects.filter(day=selected_day)  # Filter menu items by selected day
#     else:
#         menu_items = Menu.objects.all()  # Get all menu items if no day is selected

#     # Prepare context data
#     context = {
#         'breakfast_items': menu_items.filter(menu_type='breakfast'),
#         'lunch_items': menu_items.filter(menu_type='lunch'),
#         'tea_snack_items': menu_items.filter(menu_type='tea_snacks'),
#         'dinner_items': menu_items.filter(menu_type='dinner'),
#         'special_items': menu_items.filter(menu_type='special'),
#         'selected_day': selected_day,  # Pass the selected day to the template
#     }

#     return render(request, 'menu_item/manage.html', context)

# def manage(request):
#     if request.method == 'POST':
#         day = request.POST.get('day')
#         breakfast_item = request.POST.get('breakfast_items')
#         lunch_item = request.POST.get('lunch_items')
#         tea_snack_item = request.POST.get('tea_snack_items')
#         dinner_item = request.POST.get('dinner_items')
#         special_item_name = request.POST.get('special_item_name')
#         price = request.POST.get('price')

#         # Assuming you have a MenuItem model defined
#         if breakfast_item:
#             Menu.objects.create(day=day, menu_type='breakfast', item_name=breakfast_item)
#         if lunch_item:
#             Menu.objects.create(day=day, menu_type='lunch', item_name=lunch_item)
#         if tea_snack_item:
#             Menu.objects.create(day=day, menu_type='tea_snack', item_name=tea_snack_item)
#         if dinner_item:
#             Menu.objects.create(day=day, menu_type='dinner', item_name=dinner_item)
#         if special_item_name and price:
#             Menu.objects.create(day=day, menu_type='special', item_name=special_item_name, price=price)

#         return redirect('manage')  # Redirect to the manage page

#     # GET request: Fetch the existing menu items
#     selected_day = request.GET.get('day', 'Monday')  # Default to Monday if no day is selected
#     breakfast_items = Menu.objects.filter(day=selected_day, menu_type='breakfast')
#     lunch_items = Menu.objects.filter(day=selected_day, menu_type='lunch')
#     tea_snack_items = Menu.objects.filter(day=selected_day, menu_type='tea_snack')
#     dinner_items = Menu.objects.filter(day=selected_day, menu_type='dinner')
#     special_items = Menu.objects.filter(day=selected_day, menu_type='special')

#     context = {
#         'selected_day': selected_day,
#         'breakfast_items': breakfast_items,
#         'lunch_items': lunch_items,
#         'tea_snack_items': tea_snack_items,
#         'dinner_items': dinner_items,
#         'special_items': special_items,
#     }
#     return render(request, 'menu_item/manage.html', context)

# def manage(request):
#     # Fetch menu items based on menu_type
#     breakfast_items = Menu.objects.filter(menu_type='breakfast')
#     lunch_items = Menu.objects.filter(menu_type='lunch')
#     tea_snack_items = Menu.objects.filter(menu_type='tea_snacks')
#     dinner_items = Menu.objects.filter(menu_type='dinner')
#     special_items = Menu.objects.filter(menu_type='special')

#     context = {
#         'breakfast_items': breakfast_items,
#         'lunch_items': lunch_items,
#         'tea_snack_items': tea_snack_items,
#         'dinner_items': dinner_items,
#         'special_items': special_items,
#     }

#     return render(request, 'menu_item/manage.html', context)


def delete_item(request, idd):
    item = get_object_or_404(Menu, pk=idd)
    item.delete()  # Delete the item from the database
    return redirect('manage') 

# def delete(request,idd):
#     obj=Student.objects.get(mess_id=idd)
#     obj.delete()
#     return ms(request)

#view menu
# def vm(request):
#     selected_day = request.GET.get('day')

#     if selected_day:
#         breakfast_menu = Menu.objects.filter(day=selected_day, menu_type='breakfast')
#         lunch_menu = Menu.objects.filter(day=selected_day, menu_type='lunch')
#         dinner_menu = Menu.objects.filter(day=selected_day, menu_type='dinner')
#         special_menu = Menu.objects.filter(day=selected_day).first()  # Assuming you want the first special menu for the day
#     else:
#         breakfast_menu = lunch_menu = dinner_menu = special_menu = None

#     return render(request, 'menu_item/view_menu.html', {
#         'selected_day': selected_day,
#         'breakfast_menu': breakfast_menu,
#         'lunch_menu': lunch_menu,
#         'dinner_menu': dinner_menu,
#         'special_menu': special_menu,
#     })


