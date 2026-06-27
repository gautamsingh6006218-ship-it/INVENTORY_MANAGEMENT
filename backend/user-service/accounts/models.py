from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_Admin(self):
        return self.role == 'admin'

    def is_Staff_member(self):
        return self.role == 'staff'
    
    def get_full_details(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'phone': self.phone,
        }
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    