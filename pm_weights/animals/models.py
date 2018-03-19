from django.db import models

# Create your models here.

class Animal(models.Model):
    # bookkeeping fields
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
class AnimalWeight(models.Model):
    # bookkeeping fields
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # fields of importance
    animal = models.ForeignKey(Animal)
    weight = models.FloatField()
    weigh_date = models.DateTimeField()