from django.shortcuts import render
from django.http import HttpResponse
from nasdaq_stock.models import CompanyInfo
import operator
from django.db.models import IntegerField
from django.db.models.functions import Cast

# Create your views here.
def main(request):
    companies = CompanyInfo.objects.annotate(int_sales = Cast('sales', IntegerField())).order_by('-int_sales')[:10]
    symbol = []
    sales = []
    employees = []
    for company in companies:
        symbol.append(company.stock_symbol)
        sales.append(company.sales)
        employees.append(company.employees)
    dbData = { 
        "symbol": symbol,
        "sales": sales, 
        "employees": employees
    }
    return render(request, 'contents/main.html', dbData)

def macroMap(request):
    data = []
    return render(request, 'contents/maps.html')