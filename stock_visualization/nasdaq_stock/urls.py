from django.urls import path
from nasdaq_stock import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('top_companies/', views.topCompanies, name = 'top_companies'),
    path('company_list/', views.companyList, name = 'companyList'),
    path('company_list/<str:symbol>/', views.companyDetail, name='companyDetail'),
]
