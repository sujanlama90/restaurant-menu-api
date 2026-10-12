from django.db import models
from accounts.models import CustomUser
from menu.models import FoodItem
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cart(models.Model):
    customer =models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='cart')
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT,related_name='cart_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)])
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "food_item"],
                name="unique_food_item_per_cart"
            )
        ]