from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('',index, name='dash'),
    path('login/',login, name='login'),
    path('logout/',logout_view, name='logout'),
    path('signup/',signup, name='signup'),
    path('profile/', profile_view, name='profile'),
]