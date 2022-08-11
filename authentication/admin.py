from django.contrib import admin

from .models import Role, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions", "groups"]
    readonly_fields = ["password", "last_login"]
    list_display = ["id", "username", "first_name", "last_name", "age", "phone", "role"]     
    list_filter = ["age"]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
