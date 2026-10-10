from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120,unique=True)
    description= models.TextField(blank=True)
    image = models.ImageField(upload_to='categories',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now_add=True)
    class Meta: constraints = [models.UniqueConstraint( 
        Lower("name"),
        name="unique_category_name_ci" ) 
        ] 


class FoodItem(models.Model):
    FOOD_TYPE_CHOICES = [
        ("VEGETARIAN", "Vegetarian"),
        ("NON_VEGETARIAN", "Non-vegetarian"),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='foods')
    name = models.CharField(max_length=150)
    slug= models.SlugField(max_length=170,unique=True)
    description= models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='foods',blank=True,null=True)
    food_type = models.CharField(choices=FOOD_TYPE_CHOICES)
    is_available = models.BooleanField(default=True)
    preparation_time =models.PositiveSmallIntegerField()
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
