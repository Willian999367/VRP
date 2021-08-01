#coding: utf-8
from django.urls import path 
from .import views


urlpatterns = [
    path('map/', views.Index.as_view(), name='map'),

]


