from django.contrib import admin

from .models import ItemInStore, ItemOnEmpl, Employee

@admin.register(ItemInStore)
class ItemInStoreDefined(admin.ModelAdmin):
    readonly_field = ("total_price", )
    list_display = (
        "name", "model", "serie",
        "quantity", "unit_price",
        "total_price",
    )

@admin.register(ItemOnEmpl)
class ItemOnEmplDefined(admin.ModelAdmin):
    readonly_field = ("total_price", )
    list_display = (
        "name", "model", "serie",
        "quantity", "unit_price",
        "total_price", "onhand_quantity"
    )

@admin.register(Employee)
class EmployeeDefined(admin.ModelAdmin):
    pass

admin.site.site_header = "Hararii TVET Agency Inventory"

