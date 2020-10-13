from django.urls import path
from . import views
from django.conf import settings


urlpatterns= [
    path('hi',views.user_home,name='user_home'),
    # path('virtual',views.virtual,name='virtual')

]