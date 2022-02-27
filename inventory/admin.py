from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html

from .models import Employee, IncomingItem, InstoreItem, OnHandItem, OrderByEmployee

@admin.register(InstoreItem)
class InstoreItemDefined(admin.ModelAdmin):
    search_fields = ("name", "model", "serie", )
    readonly_field = ("total_price", "name", "model", "serie", "quantity")
    list_filter = ('name', 'model', 'serie')
    list_display = (
        "name", "model", "serie",
        "quantity", "check_out"
    )

    def check_out(self, obj):
        url = reverse('check-out', kwargs={'pk':obj.pk})
        return format_html(
            f'<a href="{url}" class="button">Check Out</a>'
        )
    check_out.short_description = "Check out an item"
    check_out.allow_tags = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(IncomingItem)
class IncomingItemDefined(admin.ModelAdmin):
    search_fields = ("name", "model", "serie", )
    list_display = (
        "name", "model", "serie",
        "quantity", "unit_price",
        "total_price", "registered_date"
    )
    exclude = (
        "total_price", 
        "registered_date"
    )
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OnHandItem)
class OnHandItemDefined(admin.ModelAdmin):
    search_fields = ("name", "model", "serie", "employee",)
    list_filter = ('employee',)
    list_display = (
        "name", "model", "serie",
        "quantity", 'employee',
        "check_in",
    )

    def check_in(self, obj):
        url = reverse('check-in', kwargs={'pk':obj.pk})
        return format_html(
            f'<a href="{url}" class="button">Check In</a>'
        )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Employee)
class EmployeeDefined(admin.ModelAdmin):
    list_display = ('name', 'employee_id',)

@admin.register(OrderByEmployee)
class OrderByEmployeeDefined(admin.ModelAdmin):
    list_display = (
        'name', 'description', 
        'approved_by_store_mgmt',
        'approved_by_agency_dire',
    )
    list_filter = (
        'name', 
        'approved_by_store_mgmt',
        'approved_by_agency_dire',
    )
    search_fields = ('name', 'discription')


    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.site_header = "Hararii TVET Agency Inventory"
