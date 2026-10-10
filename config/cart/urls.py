from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CartView
router = DefaultRouter()
router.register('',CartView,basename='cart')
urlpatterns = [
    path('',include(router.urls))
]
