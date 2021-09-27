from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User

class UpdatedUserAdmin(UserAdmin):
    list_display = ('username', 'userPlan', 'is_superuser', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('User Plan', {'fields': ('userPlan', )}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups','user_permissions', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined', )})
    )
    
admin.site.register(User, UpdatedUserAdmin)
admin.site.unregister(Group)