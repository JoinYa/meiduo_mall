from django.contrib import admin
from .models import User, Addr, Area


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'mobile', 'avatar', 'is_staff', 'is_superuser', 'is_active', 'is_deleted', 'create_time')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_deleted')
    search_fields = ('username', 'email')


@admin.register(Addr)
class AddrAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'mobile', 'province', 'city', 'county', 'address', 'is_default', 'create_time')
    list_filter = ('user', 'name', 'mobile')
    search_fields = ('user', 'name')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    list_filter = ('name', 'level')
    search_fields = ('name', 'level')
