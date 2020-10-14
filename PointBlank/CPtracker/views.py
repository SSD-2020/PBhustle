from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def userhome(request):
    return render(request,'userhome.html')

def codeforces(request):
    return render(request,'codeforces.html')

def codechef(request):
    return render(request,'codechef.html')

def hackerrank(request):
    return render(request,'hackerrank.html')

def pbhustle(request):
    return render(request,'pbhustle.html')