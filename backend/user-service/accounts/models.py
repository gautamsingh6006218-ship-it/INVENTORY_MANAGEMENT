from django.contrib.auth.models import AbstractUser
from django.db import models

# Inherits from AbstractUser to reuse Django's built-in auth logic
# (password hashing, login, permissions) and extend it with custom fields
class User(AbstractUser):

    # Restricts role to only two allowed values stored in database
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )

    # Overrides AbstractUser email to enforce uniqueness — used as login field
    email = models.EmailField(unique=True)
    # Controls what actions user can perform in the system
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    # Optional contact info, not required during registration
    phone = models.CharField(max_length=15, blank=True, null=True)
    # Auto-set on creation, never changes — useful for audit tracking
    created_at = models.DateTimeField(auto_now_add=True)
    # Auto-updates on every save — tracks last modification
    updated_at = models.DateTimeField(auto_now=True)

    # Makes email the login identifier instead of default username
    USERNAME_FIELD = 'email'
    # username still required internally by AbstractUser
    REQUIRED_FIELDS = ['username']

    # Encapsulation — hides role check logic, reused across views and services
    def is_Admin(self):
        return self.role == 'admin'

    # Encapsulation — single place to update if staff logic changes
    def is_Staff_member(self):
        return self.role == 'staff'

    # Returns only safe fields — password excluded intentionally
    def get_full_details(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'phone': self.phone,
        }

    # Controls how user appears in Django admin panel and print statements
    def __str__(self):
        return f"{self.email} ({self.role})"

    