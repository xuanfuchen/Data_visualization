from asyncio.windows_events import NULL
from collections import defaultdict
from copy import deepcopy
from django.shortcuts import render
from nasdaq_stock.models import CompanyInfo, PriceHistory
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def home(request):
    # ========================================================== get data for top 10 sectors by sales =============================================
    top_sales_sector_name_list = []
    top_sales_sector_value_list = []
    allComp = CompanyInfo.objects.all()
    sector_sales_total_dict = defaultdict(int)
    sector_sales_total_list = []
    for company in allComp:
        if(company.sector == "-"):
            sector_sales_total_dict["Undefined"] += int(company.sales)
        else:
            sector_sales_total_dict[company.sector] += int(company.sales)

    top_dict = sorted(sector_sales_total_dict.items(), key = lambda item: item[1], reverse=True)[:10]
    for x in top_dict:
        dict = {'value': x[1], 'name': x[0]}
        sector_sales_total_list.append(dict)
        top_sales_sector_name_list.append(x[0])
        top_sales_sector_value_list.append(x[1])
    
    # ========================================================== get data for maps ==========================================================
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

    #========================================================== get data for top 10 sectors by total employees ==========================================================
    top_employees_sector_name_list = []
    top_employees_sector_value_list = []
    sector_employees_total_list = []

    sector_employees_total_dict = defaultdict(int)
    for company in allComp:
        if(company.sector == "-" or company.sector == "Undefined"):
            pass
        else:
            sector_employees_total_dict[company.sector] += int(company.employees)

    employees_top_dict = sorted(sector_employees_total_dict.items(), key = lambda item: item[1], reverse=True)[:10]
    for x in employees_top_dict:
        dict = {'value': x[1], 'name': x[0]}
        sector_employees_total_list.append(dict)
        top_employees_sector_name_list.append(x[0])
        top_employees_sector_value_list.append(x[1])
    
    #========================================================== get data for top 10 sectors by numbers ==========================================================
    top_number_sector_name_list = []
    top_number_sector_value_list = []
    sector_bumber_total_list = []

    sector_number_total_dict = defaultdict(int)
    for company in allComp:
        if(company.sector == "-" or company.sector == "Undefined"):
            pass
        else:
            sector_number_total_dict[company.sector] += 1

    number_top_dict = sorted(sector_number_total_dict.items(), key = lambda item: item[1], reverse=True)[:10]
    for x in number_top_dict:
        dict = {'value': x[1], 'name': x[0]}
        sector_bumber_total_list.append(dict)
        top_number_sector_name_list.append(x[0])
        top_number_sector_value_list.append(x[1])

    # ========================================================== sent data to the front-end ===================================================
    dbData = { 
        #send data for top 10 sectors by sales
        "top_sales_sector_name_list": top_sales_sector_name_list,
        "top_sales_sector_value_list": top_sales_sector_value_list,
        "sector_sales_total_list": sector_sales_total_list,

        #send data for maps
        "count_list": count_list,
        "sales_list": sales_list,
        "country_count": country_count,
        "comp_count": comp_count,
        "country_sales": country_sales,
        "comp_sales": comp_sales,

        #send data for top 10 sectors by total employees
        "top_employees_sector_name_list": top_employees_sector_name_list,
        "top_employees_sector_value_list": top_employees_sector_value_list,
        "sector_employees_total_list": sector_employees_total_list,
        
        #send data for top 10 sectors by numbers
        "top_number_sector_name_list": top_number_sector_name_list,
        "top_number_sector_value_list": top_number_sector_value_list,
        "sector_bumber_total_list": sector_bumber_total_list,
    }
    return render(request, 'contents/home.html', dbData)



def topCompanies(request):
    #========================================================== get top 10 companies by sales ==========================================================
    topCompanies = CompanyInfo.objects.annotate(int_sales = Cast('sales', IntegerField())).order_by('-int_sales')[:10]
    compNameList = []
    symbolList = []
    salesList = []
    employees = []
    industry = []
    country_dict = defaultdict(int)
    top_ten_sales_pie_data = [] #[{value: sales, name: company}, {value: sales, name: company} ...]
    for company in topCompanies:
        compNameList.append(company.company_name)
        symbolList.append(company.stock_symbol)
        salesList.append(company.sales)
        employees.append(company.employees)
        industry.append(company.industry)
        country_dict[company.country] += 1
        top_ten_sales_pie_data.append({'value': company.sales, 'name': company.company_name})
    
    country_dict = sorted(country_dict.items(), key = lambda x: x[1], reverse=True)
    country_name = []
    country_count = []
    for x in country_dict:
        country_name.append(x[0])
        country_count.append(x[1])
    
    # ========================================================== get data for sales line chart ==========================================================
    # need a list [
    # ['dates', date, date, date ... ...]
    # ['comp_1', price, price, price ...]
    # ['comp_2', price, price, price ...]
    # ... ...
    # ]


    # first get all dates that top 10 companies have record
    salesDateList = []
    for topCompany in topCompanies:
        symbol = topCompany.stock_symbol
        topPriceHistory = PriceHistory.objects.filter(stock_symbol = symbol)
        for dayPrice in topPriceHistory:
            if dayPrice.price_date not in salesDateList:
                salesDateList.append(dayPrice.price_date)
    salesDateList = sorted(salesDateList)

    # create the first list in the return list
    salesDates = ['dates']
    for date in salesDateList:
        salesDates.append(date.strftime("%b %d"))
    
    # create the list that will be sent to the front-end
    salesLineChartData = []
    salesLineChartData.append(salesDates)

    for topCompany in topCompanies:
        # iterate the top company list, topCompany belongs to CompanyInfo.objects
        companyPriceList = []
        symbol = topCompany.stock_symbol
        companyPriceList.append(symbol)
        # iterate through every possible date
        for date in salesDateList:
            # try to find corrispond price to the date, and add it to the list for that company
            try:
                datePrice = PriceHistory.objects.get(stock_symbol = symbol, price_date=date)
                price = datePrice.close
                companyPriceList.append(float(price))
            # if the data doesn't exist, put a null there as a placeholder
            except:
                companyPriceList.append(NULL)
        
        # add the list to the return list
        salesLineChartData.append(companyPriceList)


    dbData = {
        "compName": compNameList,
        "comp_symbol": symbolList,
        "sales": salesList, 
        "employees": employees,
        "salesLineChartData": salesLineChartData,
        "country_name": country_name,
        "country_count": country_count,
        "top_ten_sales_pie_data": top_ten_sales_pie_data,

    }
    return render(request, 'contents/topCompanies.html', dbData)


def companyList(request):

    search = request.GET.get('search')

    if search:
        companyList = CompanyInfo.objects.filter(Q(company_name__icontains = search) | Q(stock_symbol__icontains = search))
    else:
        # if there's no search, request.GET.get('search') will be "None", so we need to reset it to empty string
        search = ''
        companyList = CompanyInfo.objects.all()

    paginator = Paginator(companyList, 100)
    page = request.GET.get('page')

    companies = paginator.get_page(page)

    count = companies.__len__

    dbData = { 
        "companies": companies,
        "search": search,
        "count": count
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