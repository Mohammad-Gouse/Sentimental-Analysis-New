from django.db import models

# Create your models here.
class Review(models.Model):
    user_name = models.CharField(max_length=50)
    description = models.TextField()
    response = models.CharField(max_length=10)