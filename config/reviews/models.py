from django.db import models
from accounts.models import CustomUser
from menu.models import FoodItem
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Review(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='reviews')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE,related_name='reviews')
    rating = models.PositiveIntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],help_text="Rating must be an integer between 1 and 5.",)
    comment = models.TextField()
    is_approved =models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "food_item"],
                name="unique_customer_food_review",
            )
        ]

    def __str__(self):
        return f"{self.customer} - {self.food_item} ({self.rating}/5)"