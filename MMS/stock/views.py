from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stock.models import Stock

from django.shortcuts import render
from .models import Stock  # Import your Stock model

def stock(request):
    obk = ""
    item_code_error = ""

    if request.method == "POST":
        item_code = request.POST.get('item_code')

        # Check if the item code already exists
        if Stock.objects.filter(item_code=item_code).exists():
            item_code_error = "Error: Item code already exists."
        else:
            obj = Stock()
            obj.item_code = item_code
            obj.item_name = request.POST.get('item_name')
            obj.stock_quantity = request.POST.get('quantity')
            obj.threshold = request.POST.get('threshold')
            obj.price = request.POST.get('price')
            obj.save()
            obk = "Successfully Added"

    # Fetch all existing stock items
    stocks = Stock.objects.all()

    context = {
        'msg': obk,
        'item_code_error': item_code_error,
        'stocks': stocks  # Pass the list of stocks to the template
    }
    
    return render(request, 'stock/stock.html', context)


def update_stock(request, stock_id):
    # Fetch the stock object based on the 'stock_id'
    stock_item = Stock.objects.get(stock_id=stock_id)
    
    if request.method == "POST":
        # Update the stock object with form data
        stock_item.item_name = request.POST.get('item_name')
        stock_item.stock_quantity = request.POST.get('stock_quantity')
        stock_item.threshold = request.POST.get('threshold')
        stock_item.price = request.POST.get('price')

        # Save the updated stock object
        stock_item.save()

        # Redirect after updating to prevent old form data from appearing
        return mansto(request)  # Assuming there's a stock list view

    # Prepare the context with the latest stock data
    context = {
        'stock': stock_item
    }
    
    # Render the form with the stock data
    return render(request, 'stock/update.html', context)


def mansto(request):
    obj=Stock.objects.all()
    context={
        'stocks':obj
    }
    return render(request,'stock/manage_stock.html',context)



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
    

def delete(request,idd):
    obj=Stock.objects.get(stock_id=idd)
    obj.delete()
    return mansto(request)

# def delete(request,idd):
#     obj=Student.objects.get(mess_id=idd)
#     obj.delete()
#     return ms(request)
