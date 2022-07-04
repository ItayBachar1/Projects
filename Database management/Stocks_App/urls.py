from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Query', views.Query, name='Query'),
    path('Buy', views.Buy, name='Buy'),
    path('Add', views.Add, name='Add')
]