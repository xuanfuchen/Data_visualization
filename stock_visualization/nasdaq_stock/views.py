from asyncio.windows_events import NULL
from collections import defaultdict
from copy import deepcopy
from django.shortcuts import render
from nasdaq_stock.models import CompanyInfo, PriceHistory
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.
def main(request):
    # ========================================================== data for bar chart and pie chart =============================================
    topCompanies = CompanyInfo.objects.annotate(int_sales = Cast('sales', IntegerField())).order_by('-int_sales')[:10]
    compNameList = []
    symbolList = []
    salesList = []
    employees = []
    for company in topCompanies:
        compNameList.append(company.company_name)
        symbolList.append(company.stock_symbol)
        salesList.append(company.sales)
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
    

    # ========================================================== data for line chart ==========================================================
    # need a list [
    # ['dates', date, date, date ... ...]
    # ['comp_1', price, price, price ...]
    # ['comp_2', price, price, price ...]
    # ... ...
    # ]


    # first get all dates that top 10 companies have record
    dateList = []
    for topCompany in topCompanies:
        symbol = topCompany.stock_symbol
        topPriceHistory = PriceHistory.objects.filter(stock_symbol = symbol)
        for dayPrice in topPriceHistory:
            if dayPrice.price_date not in dateList:
                dateList.append(dayPrice.price_date)
    dateList = sorted(dateList)

    # create the first list in the return list
    dates = ['dates']
    for date in dateList:
        dates.append(date.strftime("%b %d"))
    
    # create the list that will be sent to the front-end
    lineChartData = []
    lineChartData.append(dates)

    for topCompany in topCompanies:
        # iterate the top company list, topCompany belongs to CompanyInfo.objects
        companyPriceList = []
        symbol = topCompany.stock_symbol
        companyPriceList.append(symbol)
        # iterate through every possible date
        for date in dateList:
            # try to find corrispond price to the date, and add it to the list for that company
            try:
                datePrice = PriceHistory.objects.get(stock_symbol = symbol, price_date=date)
                price = datePrice.close
                companyPriceList.append(float(price))
            # if the data doesn't exist, put a null there as a placeholder
            except:
                companyPriceList.append(NULL)
        
        # add the list to the return list
        lineChartData.append(companyPriceList)

    # ========================================================== sent data to the front-end ===================================================
    dbData = { 
        "compName": compNameList,
        "comp_symbol": symbolList,
        "sales": salesList, 
        "employees": employees,
        "sector_total_list": sector_total_list,
        "lineChartData": lineChartData,
    }
    return render(request, 'contents/main.html', dbData)



def macroMap(request):
    count_dict = defaultdict(int)
    sales_dict = defaultdict(int)
    companies = CompanyInfo.objects.all()
    count_list = []
    sales_list = []

    country_count = []
    comp_count = []
    country_sales = []
    comp_sales = []
    for company in companies:
        if company.country == "-":
            # count_dict["Unknown"] += 1
            pass
        else:
            count_dict[company.country] += 1
            sales_dict[company.country] += int(company.sales)

    
    sorted_count = sorted(count_dict.items(), key = lambda item: item[1], reverse=True)
    for x in sorted_count:
        dict = {'name': x[0], 'value': x[1]}
        count_list.append(dict)
    
    for x in sorted_count[:20]:
        country_count.append(x[0])
        comp_count.append(x[1])
    
    sorted_sales = sorted(sales_dict.items(), key = lambda item: item[1], reverse=True)
    for x in sorted_sales:
        dict = {'name': x[0], 'value': x[1]}
        sales_list.append(dict)

    for x in sorted_sales[:20]:
        country_sales.append(x[0])
        comp_sales.append(x[1])

    dbData = {
        "count_list": count_list,
        "sales_list": sales_list,
        "country_count": country_count,
        "comp_count": comp_count,
        "country_sales": country_sales,
        "comp_sales": comp_sales
    }
    return render(request, 'contents/maps.html', dbData)


def companyList(request):
    # get all company info from model CompanyInfo
    companyList = CompanyInfo.objects.all()

    paginator = Paginator(companyList, 100)
    page = request.GET.get('page')

    companies = paginator.get_page(page)

    dbData = { 
        "companies": companies,
    }

    return render(request, 'contents/companyList.html', dbData)



def companyDetail(request, symbol):
    companyDetail = CompanyInfo.objects.get(stock_symbol = symbol)

    companyPriceHistory = PriceHistory.objects.filter(stock_symbol = symbol)

    categoryData = []
    valueData = []
    volumeData = []
    
    lineCategory = []
    lineValue = []

    for companyPrice in companyPriceHistory:
        dateStr = companyPrice.price_date.strftime("%b %d")
        
        # gather data for candlestick chart
        categoryData.append(dateStr)
        valueList = [companyPrice.open, companyPrice.close, companyPrice.low, companyPrice.high]
        valueData.append(valueList)
        volumeData.append(companyPrice.volume)

        # gather data for line chart
        lineCategory.append(dateStr)
        lineValue.append(companyPrice.close)



    dbData = {
        "companyDetail": companyDetail,
        "categoryData": categoryData,
        "valueData": valueData,
        "volumeData": volumeData,
        "lineCategory": lineCategory,
        "lineValue": lineValue

        
    }

    return render(request, 'contents/companyDetail.html', dbData)