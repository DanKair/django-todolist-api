from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name