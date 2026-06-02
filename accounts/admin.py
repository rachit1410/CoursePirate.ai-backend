from django.contrib import admin
from accounts.models import Pirate

@admin.register(Pirate)
class PirateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_active')
    list_filter = ('name', 'email', 'is_staff', 'is_active')
    search_fields = ('name', 'email', 'is_staff', 'is_active')
