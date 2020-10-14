from django.urls import path
from . import views
from django.conf import settings


urlpatterns= [
    path('',views.userhome,name='userhome'),
    path('codeforcesuserinfo/', views.codeforcesuserinfo , name='codeforcesuserinfo'),
    path('codeforcesrating/', views.codeforcesrating , name='codeforcesrating'),
    path('codechef/', views.codechef , name='codechef'),
    path('hackerrank/', views.hackerrank, name='hackerrank'),
    path('pbhustle/', views.pbhustle , name='pbhustle'),

]