from django.contrib import admin
from .models import RBACUser, UserRole, RolePermission, Role, Permission

class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1  # Number of empty forms to show in the admin interface

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name', 'description']
    search_fields = ['role_name', 'description']  # Enable search functionality
    inlines = [RolePermissionInline]  # Add RolePermission inline to the Role admin form

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission_name', 'description']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    search_fields = ['user__username', 'role__role_name']  # Enable searching by username or role name
    list_filter = ['role']  # Add a filter by role
    autocomplete_fields = ['user', 'role']  # Use autocomplete for user and role fields

@admin.register(RBACUser)
class RBACUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved', 'is_active']
    list_filter = ['is_approved', 'is_active']
    search_fields = ['username', 'email']
    filter_horizontal = ['roles']  # Adds a horizontal multi-select for roles


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission']