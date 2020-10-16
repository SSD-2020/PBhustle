from django.urls import path
from . import views
from django.conf import settings


urlpatterns= [

    path('',views.landingpage,name='landingpage'),
    path('userhome/',views.userhome,name='userhome'),
    path('userhome/codeforces/', views.codeforces, name='codeforces'),
    path('userhome/codeforces/codeforcesCompare/', views.codeforcesCompare, name='codeforcesCompare'),
    path('userhome/codechef/', views.codechef , name='codechef'),
    path('userhome/codechef/codechefCompare/', views.codechefCompare, name='codechefCompare'),
    path('userhome/hackerrank/', views.hackerrank, name='hackerrank'),
    path('userhome/pbhustle/', views.pbhustle , name='pbhustle'),

]