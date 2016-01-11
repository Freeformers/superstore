from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse_lazy

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=200)
    
    def get_absolute_url(self):
        return reverse_lazy('shop-department', kwargs={'pk': self.pk})
        
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=10)
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='products')
    
    COLOURS = [
        (1, 'Red'),
        (2, 'Blue'),
        (3, 'Yellow'),
        (4, 'Green'),
        (5, 'White'),
        (6, 'Black'),
    ]
    
    colour = models.IntegerField(choices=COLOURS, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    score = models.IntegerField()
    content = models.TextField()