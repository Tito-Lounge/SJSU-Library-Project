"""
URL configuration for sjsulibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from rbac import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('manage-inventory/', views.manage_inventory, name='manage_inventory'),
    path('assign-role/', views.assign_role, name='assign_role'),
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('university-resources/', views.university_resources, name='university_resources'),
    path('place-hold/', views.place_hold, name='place_hold'),
    path('public-resources/', views.public_resources, name='public_resources'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('user-list/', views.user_list, name='user_list'),
    path('provision-user/', views.provision_user, name='provision_user'),
]
