from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        role = "Kutubxonachi" if self.is_librarian else "Admin"
        return f"{self.username} ({role})"