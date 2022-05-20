from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(request):
    return render(request, 'contents/main.html')

def macroMap(request):
    data = []
    return render(request, 'contents/maps.html')