from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from hotel import views as hotel_views

urlpatterns = [
    path('admin/', admin.site.urls),


    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


    path('staff/', hotel_views.staff_dashboard, name='staff_dashboard'),


    path('', include('hotel.urls')),
]
