from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token

from .manager import CustomUserManager
from utils.get_utc_time import get_utc_time

role_choices = (
    ('super_admin','Super Admin'),
    ('customer', 'Customer')
)


class User(AbstractBaseUser):
    email = models.EmailField(null=False, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=12, choices=role_choices, null=False, default='customer')
    address = models.CharField(max_length=255, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def delete(self , request):
        self.delete_tokens()
        self.is_deleted = True
        self.deleted_at = get_utc_time()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def delete_tokens(self):
        Token.objects.filter(user=self).delete()

    class Meta:
        db_table = 'users'
