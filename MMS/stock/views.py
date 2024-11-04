from django.shortcuts import render
from stock.models import Stock
from django.db.models import F
# Create your views here.

from django.db.models import F
from django.shortcuts import render

from django.shortcuts import render
from .models import Stock
from django.db.models import F

def stock(request):
    obk = ""
    item_code_error = ""
    threshold_error = ""

    if request.method == "POST":
        item_code = request.POST.get('item_code')
        stock_quantity = int(request.POST.get('stock_quantity'))  # Convert to integer
        threshold = int(request.POST.get('threshold'))  # Convert to integer

        # Check if the item code already exists
        if Stock.objects.filter(item_code=item_code).exists():
            item_code_error = "Item code already exists."
        # Check if the quantity is valid (i.e., stock_quantity < threshold)
        elif stock_quantity <= threshold:
            threshold_error = "Quantity cannot be less than or equal to the threshold."
        else:
            # Save the new stock item
            obj = Stock()
            obj.item_code = item_code
            obj.item_name = request.POST.get('item_name')
            obj.stock_quantity = stock_quantity
            obj.threshold = threshold
            obj.price = request.POST.get('price')
            obj.save()
            obk = "Stock Successfully Added"
    
    # Fetch all existing stock items
    stocks = Stock.objects.all()

    # Count the number of items that are low in stock (i.e., stock_quantity <= threshold)
    low_stock_count = Stock.objects.filter(stock_quantity__lte=F('threshold')).count()

    context = {
        'msg': obk,
        'item_code_error': item_code_error,
        'threshold_error': threshold_error,  # Pass the threshold error to the template
        'stocks': stocks,  # Pass the list of stocks to the template
        'low_stock_count': low_stock_count  # Add low stock count to the context
    }
    
    return render(request, 'stock/stock.html', context)



# def stock(request):
#     obk = ""
#     item_code_error = ""

#     if request.method == "POST":
#         item_code = request.POST.get('item_code')

#         # Check if the item code already exists
#         if Stock.objects.filter(item_code=item_code).exists():
#             item_code_error = "Error: Item code already exists."
#         else:
#             obj = Stock()
#             obj.item_code = item_code
#             obj.item_name = request.POST.get('item_name')
#             obj.stock_quantity = request.POST.get('stock_quantity')
#             obj.threshold = request.POST.get('threshold')
#             obj.price = request.POST.get('price')
#             obj.save()
#             obk = "Stock Successfully Added"

#     # Fetch all existing stock items
#     stocks = Stock.objects.all()

#     context = {
#         'msg': obk,
#         'item_code_error': item_code_error,
#         'stocks': stocks  # Pass the list of stocks to the template
#     }
    
#     return render(request, 'stock/stock.html', context)


def update_stock(request, stock_id):
    # Fetch the stock object based on the 'stock_id' or return a 404 error if not found
    stock_item = Stock.objects.get(stock_id=stock_id)
    
    if request.method == "POST":
        # Update the stock object with form data
        stock_item.item_name = request.POST.get('item_name')
        stock_item.stock_quantity = int(request.POST.get('stock_quantity'))  # Cast to int
        stock_item.threshold = int(request.POST.get('threshold'))            # Cast to int
        stock_item.price = float(request.POST.get('price'))                  # Cast to float

        # Save the updated stock object
        stock_item.save()

        # Check if stock quantity is less than or equal to the threshold
        if stock_item.stock_quantity <= stock_item.threshold:
            return purchase_list(request)  # Redirect to purchase list if threshold is met
        
        # Redirect to the stock list view after updating
        return mansto(request)

    # Prepare the context with the latest stock data
    context = {
        'stock': stock_item
    }
    
    # Render the form with the stock data
    return render(request, 'stock/update.html', context)

# def update_stock(request, stock_id):
#     # Fetch the stock object based on the 'stock_id' or return a 404 error if not found
#     stock_item = Stock.objects.get(stock_id=stock_id)
    
#     if request.method == "POST":
#         # Update the stock object with form data
#         stock_item.item_name = request.POST.get('item_name')
#         stock_item.stock_quantity = int(request.POST.get('stock_quantity'))  # Cast to int
#         stock_item.threshold = int(request.POST.get('threshold'))            # Cast to int
#         stock_item.price = float(request.POST.get('price'))                  # Cast to float

#         # Save the updated stock object
#         stock_item.save()

#         # Check if stock quantity is less than or equal to the threshold
#         if stock_item.stock_quantity <= stock_item.threshold:
#             return purchase_list(request)  # Redirect to purchase list if threshold is met
        
#         # Redirect to the stock list view after updating
#         return mansto(request)  # Assuming 'stock_list' is the name of your stock list view

#     # Prepare the context with the latest stock data
#     context = {
#         'stock': stock_item
#     }
    
#     # Render the form with the stock data
#     return render(request, 'stock/update.html', context)


# def update_stock(request, stock_id):
#     # Fetch the stock object based on the 'stock_id'
#     stock_item = Stock.objects.get(stock_id=stock_id)
    
#     if request.method == "POST":
#         # Update the stock object with form data
#         stock_item.item_name = request.POST.get('item_name')
#         stock_item.stock_quantity = request.POST.get('stock_quantity')
#         stock_item.threshold = request.POST.get('threshold')
#         stock_item.price = request.POST.get('price')

#         # Save the updated stock object
#         stock_item.save()

#         # Redirect after updating to prevent old form data from appearing
#         return mansto(request)  # Assuming there's a stock list view

#     # Prepare the context with the latest stock data
#     context = {
#         'stock': stock_item
#     }
    
#     # Render the form with the stock data
#     return render(request, 'stock/update.html', context)

def mansto(request):
    # Retrieve the search queries for item code and item name from the GET request
    item_code_query = request.GET.get('item_code', '')  # Get the search query for Item Code
    item_name_query = request.GET.get('item_name', '')  # Get the search query for Item Name

    # Get all stock records
    stocks = Stock.objects.all()

    # Filter stocks based on item code if provided
    if item_code_query:
        stocks = stocks.filter(item_code__icontains=item_code_query)

    # Filter stocks based on item name if provided
    if item_name_query:
        stocks = stocks.filter(item_name__icontains=item_name_query)

    # Count the number of items that are low in stock
    low_stock_count = Stock.objects.filter(stock_quantity__lte=F('threshold')).count()

    # Pass the filtered stocks and low stock count to the template
    context = {
        'stocks': stocks,
        'low_stock_count': low_stock_count
    }

    return render(request, 'stock/manage_stock.html', context)
# def mansto(request):
#     obj=Stock.objects.all()
#     context={
#         'stocks':obj
#     }
#     return render(request,'stock/manage_stock.html',context)

def purchase_list(request):
    # Fetch stocks where stock_quantity is less than or equal to the threshold
    purchase_list = Stock.objects.filter(stock_quantity__lte=F('threshold'))

    # Count the number of items that are low in stock
    low_stock_count = purchase_list.count()
    
    return render(request, 'stock/purchase.html', {
        'purchase_list': purchase_list,
        'low_stock_count': low_stock_count  # Add low stock count to the context
    })

# def purchase_list(request):
#     # Fetch stocks where stock_quantity is less than or equal to the threshold
#     purchase_list = Stock.objects.filter(stock_quantity__lte=F('threshold'))
#     return render(request, 'stock/purchase.html', {'purchase_list': purchase_list})






# def stock(request):
#     obk=""
#     if request.method=="POST":
#         obj=Stock()
#         obj.item_code=request.POST.get('item_code')
#         obj.item_name=request.POST.get('item_name')
#         obj.stock_quantity=request.POST.get('quantity')
#         obj.threshold=request.POST.get('threshold')
#         obj.price=request.POST.get('price')
#         obj.save()
#         obk = "successfully Added"
#     context = {
#             'msg': obk
#     }
#     return render(request,'stock/stock.html',context)
    

def delete(request,stock_id):
    obj=Stock.objects.get(stock_id=stock_id)
    obj.delete()
    return mansto(request)

# def delete(request,idd):
#     obj=Student.objects.get(mess_id=idd)
#     obj.delete()
#     return ms(request)
