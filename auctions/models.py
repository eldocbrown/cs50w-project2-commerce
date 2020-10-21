from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    startingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    imageLink = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="catListings", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usrListings")
    active = models.BooleanField(default=True)
