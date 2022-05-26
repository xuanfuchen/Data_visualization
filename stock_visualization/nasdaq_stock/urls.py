from django.urls import path
from nasdaq_stock import views

urlpatterns = [
    path('main/', views.main, name = 'main'),
    path('maps/', views.macroMap, name = 'maps'),
    path('company_list/', views.companyList, name = 'companyList'),
    path('company_list/<str:symbol>/', views.companyDetail, name='companyDetail'),
]
