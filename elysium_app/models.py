from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class PlatformInfo(models.Model):
    name= models.CharField(max_length=255)
    boughtFrom = models.URLField(max_length=50)
    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=50)
    boughtFor = models.IntegerField()
    hold = models.BooleanField(default=True)
    platform = models.ForeignKey(PlatformInfo, on_delete=models.CASCADE, related_name="holder")
    number_rating = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200,null=True)
    holder = models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " - " + self.holder.name + " - "+ str(self.review_user)
    