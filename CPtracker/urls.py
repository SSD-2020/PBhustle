from django.urls import path
from . import views
from django.conf import settings


urlpatterns= [

    path('',views.landingpage,name='landingpage'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('edit/',views.edit,name='edit'),
    path('logout/',views.logout,name='logout'),
    path('userhome/',views.userhome,name='userhome'),
    path('userhome/update/',views.update,name='update'),
    path('userhome/codeforces/', views.codeforces, name='codeforces'),
    path('userhome/codeforces/update/',views.updateCF,name='updateCF'),
    path('userhome/codeforces/codeforcesCompare/', views.codeforcesCompare, name='codeforcesCompare'),
    path('userhome/pbhustle/pbhustleCompare/', views.pbhustleCompare, name='pbhustleCompare'),
    path('userhome/codechef/', views.codechef , name='codechef'),
    path('userhome/codechef/update/',views.updateCC,name='updateCC'),
    path('userhome/codechef/codechefCompare/', views.codechefCompare, name='codechefCompare'),
    path('userhome/pbhustle/', views.pbhustle , name='pbhustle'),

]