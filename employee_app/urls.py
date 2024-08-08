from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createEmployee),  
    path('get/', views.getEmployee),
    path('get/<str:regid>/', views.getEmployee),
    path('update/<str:regid>/', views.updateEmployee),
    path('delete/<str:regid>/', views.deleteEmployee),   
   
   
]