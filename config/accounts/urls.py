from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import CustomerRegisterView,AdminRegisterView,StaffRegisterView,LoginView,Profile,UserListView
router = DefaultRouter()
router.register('register/customer',CustomerRegisterView,basename='customer_register')
router.register('register/staff',StaffRegisterView,basename='staff_register')
router.register('register/admin',AdminRegisterView,basename='admin_register')
router.register('login',LoginView,basename='login')
router.register('profile',Profile,basename='profile')
router.register('users',UserListView,basename='user_list')

urlpatterns = [
    path('',include(router.urls))
]
