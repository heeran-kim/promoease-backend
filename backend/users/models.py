from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

# MIGRATION
# docker exec -it promoease-backend-backend-1 python manage.py makemigrations users
# docker exec -it promoease-backend-backend-1 python manage.py migrate users
# ORM & API TEST
# docker exec -it promoease-backend-backend-1 python test_create_users.py

class UserManager(BaseUserManager):
    """Custom manager for the User model, handling user and supersuer creation."""

    def create_user(self, email, name, password=None, role="restaurant_owner", **extra_fields):
        """Creates and returns a regular user with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set") # Ensure email is provided
        if not name:
            raise ValueError("The Name field must be set") # Ensure name is provided
        if role not in [choice[0] for choice in User.ROLE_CHOICES]:
            raise ValueError(f"Invalid role. Choose one of: {[choice[0] for choice in User.ROLE_CHOICES]}")

        email = self.normalize_email(email) # Standardize email format
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password) # Hash and store the password
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """Creates and returns a superuser with full permissions."""
        extra_fields.setdefault("is_staff", True) # Required for Django Admin access
        extra_fields.setdefault("is_superuser", True) # Gives all permissions
        extra_fields.setdefault("role", "admin")

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model using email as the unique identifier."""

    # Use role field instead of Django's Groups & Permissions
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('restaurant_owner', 'Restaurant Owner'),
    )

    email = models.EmailField(unique=True) # Primary unique identifier for login
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='restaurant_owner') # User role
    is_active = models.BooleanField(default=True) # Determines if the user can log in
    is_staff = models.BooleanField(default=False) # Needed for Django Admin panel access
    date_joined = models.DateTimeField(auto_now_add=True) # Stores when the user registered

    objects = UserManager() # Assign custom UserManager for object creation

    USERNAME_FIELD = "email" # Use email as the unique login field
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email # String representation of the user

    def is_admin(self):
        """Returns True if the user is an admin."""
        return self.role == "admin"

    def get_short_name(self):
        return self.name