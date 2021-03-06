from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group, User

from .models import Employee, IncomingItem, InstoreItem, OnHandItem, OrderByEmployee

@admin.register(InstoreItem)
class InstoreItemDefined(admin.ModelAdmin):
    search_fields = ("name", "model", "serie", )
    readonly_field = ("total_price", "name", "model", "serie", "quantity")
    list_filter = ('name', 'model', 'serie', 'type')
    list_display = (
        "name", "model", "serie",
        "quantity", "type", "check_out"
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
    search_fields = ("name", "model", "serie", "registered_date")
    list_filter = ("name", "model", "registered_date",)
    list_display = (
        "name", "model", "serie",
        "quantity", "unit_price", "type",
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
    search_fields = ("name", "model", "serie" )
    list_filter = ('name', 'model', 'serie', 'type', 'employee')
    list_display = (
        "name", "model", "serie",
        "quantity", 'employee', "type",
        "date",
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
        'approved_by_age_dir',
        'ordered_by',
    )
    list_filter = (
        'name', 
        'ordered_by',
        'approved_by_store_mgmt',
        'approved_by_age_dir',
    )
    search_fields = ('name', 'discription')
    readonly_fields = ('name', 'description', 'ordered_by')
    change_list_template = 'orderbyemployee.html'

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, change=False, **kwargs):
        fields = ['name', 'description', 'ordered_by']

        if not self.has_group(request.user, "Director"):
            fields += ['approved_by_age_dir']

        if not self.has_group(request.user, "StoreManager"):
            fields += ['approved_by_store_mgmt']
        
        self.readonly_fields = fields
        return super(OrderByEmployeeDefined, self).get_form(request, obj, **kwargs)

    def has_group(self, user, group_name):
        try:
            group = Group.objects.get(name=group_name)
            print(group)
            return True if group in user.groups.all() else False
        except Group.DoesNotExist:
            print(Exception)
            return False


site_title = "Hararii TVET Agency Inventory"
admin.site.site_header = site_title
admin.site.unregister(Group)
admin.site.unregister(User)
