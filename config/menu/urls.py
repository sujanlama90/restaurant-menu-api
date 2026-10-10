from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import Categories,FoodItemView
router = DefaultRouter()
router.register('categories',Categories,basename='Category')
router.register('foods',FoodItemView,basename='foods')

urlpatterns = [
    path('',include(router.urls)) 
]
