from stock.models import Stock
from django.db.models import F

def low_stock_count(request):
    # Check for low stock items
    low_stock_items = Stock.objects.filter(stock_quantity__lte=F('threshold'))
    return {
        'low_stock_count': low_stock_items.count(),
    }
