from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalog, name='catalog'),
    path('habitacion/<int:room_id>/', views.room_detail, name='room_detail'),
    path('reservar/<int:room_id>/', views.reserve, name='reserve'),
    path('confirmacion/<int:res_id>/', views.confirmation, name='confirmation'),
]
