from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    search_fields = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

