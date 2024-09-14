from django.db import models


class Category(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):  
        return  self.name
    
class Saved(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.TextField()
    image_url = models.TextField()
    def __str__(self):
        return self.title