from django.db import models

# Create your models here.
class CanvasImage(models.Model):
    image = models.ImageField()
    result = models.CharField(max_length=2, blank=True)
    predict = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return "Image " + str(self.id)