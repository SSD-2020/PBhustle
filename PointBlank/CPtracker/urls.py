from django.urls import path
from . import views


urlpatterns= [
    path('',views.user_home,name='user_home'),
    # path('virtual',views.virtual,name='virtual')

]