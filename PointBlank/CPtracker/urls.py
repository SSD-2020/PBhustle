from django.urls import path
from . import views
from django.conf import settings


urlpatterns= [

    path('',views.landingpage,name='landingpage'),
    path('home/',views.userhome,name='userhome'),
    path('home/codeforces/', views.codeforces, name='codeforces'),
    path('home/codeforces/codeforcesCompare/', views.codeforcesCompare, name='codeforcesCompare'),
    path('home/codechef/', views.codechef , name='codechef'),
    path('home/codechef/codechefCompare/', views.codechefCompare, name='codechefCompare'),
    path('home/hackerrank/', views.hackerrank, name='hackerrank'),
    path('home/pbhustle/', views.pbhustle , name='pbhustle'),

]