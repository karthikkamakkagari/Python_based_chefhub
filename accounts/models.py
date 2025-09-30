from django.contrib.auth.models import AbstractUser
from django.db import models

ACCOUNT_TYPE_CHOICES = (
    ('SUPREM', 'Suprem'),
    ('ADMIN', 'Admin'),
    ('USER', 'User'),
)

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('te', 'Telugu'),
    ('ta', 'Tamil'),
    ('hi', 'Hindi'),
    ('kn', 'Kannada'),
)

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class CustomUser(AbstractUser):
    token = models.PositiveIntegerField(default=0)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='USER')
    preferred_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='en')
    address = models.TextField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    catering_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
