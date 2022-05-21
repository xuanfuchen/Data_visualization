from django.shortcuts import render
from django.http import HttpResponse
from nasdaq_stock.models import CompanyInfo
import operator
from django.db.models import IntegerField
from django.db.models.functions import Cast

# Create your views here.
def main(request):
    companies = CompanyInfo.objects.annotate(int_sales = Cast('sales', IntegerField())).order_by('-int_sales')[:10]
    compName = []
    symbol = []
    sales = []
    employees = []
    for company in companies:
        compName.append(company.company_name)
        symbol.append(company.stock_symbol)
        sales.append(company.sales)
        employees.append(company.employees)
    dbData = { 
        "compName": compName,
        "symbol": symbol,
        "sales": sales, 
        "employees": employees
    }
    return render(request, 'contents/main.html', dbData)

def macroMap(request):
    return render(request, 'contents/maps.html')

def companyList(request):
    return render(request, 'contents/companyList.html')