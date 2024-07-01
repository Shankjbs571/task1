from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.state}, {self.pincode}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.png',null=False)
    line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    class Meta:
        abstract = True

class Patient(Profile):
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} (Patient)"

class Doctor(Profile):
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.user.username} (Doctor)"
