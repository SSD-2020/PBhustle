from django.urls import path
from . import views
from django.conf import settings


urlpatterns= [
    path('',views.userhome,name='userhome'),
    path('codeforces/', views.codeforces, name='codeforces'),
    path('codeforces/codeforcesCompare/', views.codeforcesCompare, name='codeforcesCompare'),
    path('codechef/', views.codechef , name='codechef'),
    path('hackerrank/', views.hackerrank, name='hackerrank'),
    path('pbhustle/', views.pbhustle , name='pbhustle'),

]