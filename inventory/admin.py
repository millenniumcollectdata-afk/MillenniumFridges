from django.contrib import admin
from .models import Location, Fridge, Transfer

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location_type", "address")
    search_fields = ("name", "address")
    list_filter = ("location_type",)

class TransferInline(admin.TabularInline):
    model = Transfer
    extra = 0
    autocomplete_fields = ("from_location", "to_location")
    readonly_fields = ("transfer_date",)

@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    list_display = ("id", "barcode", "status", "current_location", "brand", "model", "akt_no", "created_at")
    search_fields = ("barcode", "akt_no", "brand", "model")
    list_filter = ("status", "current_location")
    inlines = (TransferInline,)
    autocomplete_fields = ("current_location",)

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("id", "fridge", "from_location", "to_location", "transfer_date")
    search_fields = ("fridge__barcode",)
    list_filter = ("from_location", "to_location", "transfer_date")
    autocomplete_fields = ("fridge", "from_location", "to_location")
    readonly_fields = ("transfer_date",)
