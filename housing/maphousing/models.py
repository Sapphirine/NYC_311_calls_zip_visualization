# Author: Dwiref
# Updated: 12/20/2019

from django.db import models

# Create your models here.

class Criteria(models.Model):
    criteria = models.CharField(
        max_length = 255,
    )
