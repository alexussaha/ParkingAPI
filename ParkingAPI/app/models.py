"""
Definition of models.
"""

from django.db import models

class Parking(models.Model):
    address = models.CharField(max_length=128, blank=True, null=True, default=None)
    is_free = models.BooleanField(default=True)