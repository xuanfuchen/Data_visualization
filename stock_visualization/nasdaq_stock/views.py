from collections import defaultdict
from django.shortcuts import render
from django.http import HttpResponse
from nasdaq_stock.models import CompanyInfo
import operator
from django.db.models import IntegerField
from django.db.models.functions import Cast

# Create your views here.
def main(request):
    topCompanies = CompanyInfo.objects.annotate(int_sales = Cast('sales', IntegerField())).order_by('-int_sales')[:10]
    compName = []
    symbol = []
    sales = []
    employees = []
    for company in topCompanies:
        compName.append(company.company_name)
        symbol.append(company.stock_symbol)
        sales.append(company.sales)
        employees.append(company.employees)
    
    allComp = CompanyInfo.objects.all()
    sector_total_dict = defaultdict(int)
    sector_total_list = []
    for company in allComp:
        if(company.sector == "-"):
            sector_total_dict["Undefined"] += int(company.sales)
        else:
            sector_total_dict[company.sector] += int(company.sales)

    top_dict = sorted(sector_total_dict.items(), key = lambda item: item[1], reverse=True)[:10]
    for x in top_dict:
        dict = {'value': x[1], 'name': x[0]}
        sector_total_list.append(dict)

    dbData = { 
        "compName": compName,
        "symbol": symbol,
        "sales": sales, 
        "employees": employees,
        "sector_total_list": sector_total_list,
    }
    return render(request, 'contents/main.html', dbData)

def macroMap(request):
    return render(request, 'contents/maps.html')

def companyList(request):
    return render(request, 'contents/companyList.html')