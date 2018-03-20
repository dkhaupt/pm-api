from django.db import models

# Create your models here.

class Animal(models.Model):
    '''
    The Animal represents a single Animal in the herd
    Initially, the only field is the external ID
    '''
    # bookkeeping fields
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # fields of importance
    external_id = models.IntegerField()

    def __str__(self):
        return 'Animal {0}'.format(self.external_id)
    
class AnimalWeight(models.Model):
    '''
    The AnimalWeight model represents a weight record (weight + datetime of weighing) for a single animal
    Each Animal may have many associated AnimalWeight records
    '''
    # bookkeeping fields
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    # fields of importance
    animal = models.ForeignKey(Animal)
    weight = models.FloatField()
    weigh_date = models.DateTimeField()