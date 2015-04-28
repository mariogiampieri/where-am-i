# Create your models here.
#WhereAmI by Mario Giampieri

from django.db import models

class Coordinates(models.Model):
    x_coord = models.CharField(max_length= 20)
    y_coord = models.CharField(max_length= 20)
    # variable = models.ForeignKey(othervariable) <-Use this to create a foreign key  to connect models (so far the only model is coordinates)
