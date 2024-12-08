from django.contrib import admin
from .models import Powder, Region, Customer

@admin.register(Powder)
class PowderAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'region')
    search_fields = ('name', 'number', 'region')
