from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
# Create your models here.

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.role_name

class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length = 100, unique = True)
    description = models.TextField()

    def __str__(self):
        return self.permission_name

class RBACUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    is_approved = models.BooleanField(default=False) # Approval flag

class UserRole(models.Model):
    user = models.ForeignKey(RBACUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} | {self.role}"

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.role} | {self.permission}"