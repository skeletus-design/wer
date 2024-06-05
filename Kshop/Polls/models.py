from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2500)
    date_posted = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="images/")
    def __str__(self):
        return self.title