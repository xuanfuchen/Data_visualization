from django.urls import path
from nasdaq_stock import views

urlpatterns = [
    path('macro/', views.hello),
]
