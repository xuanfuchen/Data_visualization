from django.urls import path
from nasdaq_stock import views

urlpatterns = [
    path('main/', views.main),
    path('maps/', views.macroMap)

]
