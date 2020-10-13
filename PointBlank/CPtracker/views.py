from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def user_home(request):

    return render(request,'user_home.html')