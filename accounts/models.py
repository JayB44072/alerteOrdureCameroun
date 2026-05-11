from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citoyen', 'Citoyen'),
        ('agent', 'Agent HYSACAM'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='citoyen'
    )
    quartier = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"