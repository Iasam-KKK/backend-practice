from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Token(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20, unique=True)  # Increased to 20
    price = models.DecimalField(max_digits=20, decimal_places=10)
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class UserProfile(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL_TOKEN, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_online = models.DateTimeField(null=True, blank=True)
    REQUIRED_FIELDS = ['email']