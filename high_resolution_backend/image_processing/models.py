from django.db import models

# Create your models here.

class Images(models.Model):
    image = models.ImageField(upload_to='images')
    model_number = models.CharField(max_length=100)

    
    def __str__(self):
        return self.model_number