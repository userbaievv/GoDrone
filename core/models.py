from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurants/')
    rating = models.FloatField(default=0)

class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Dish(models.Model):
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grams = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='dishes/')
