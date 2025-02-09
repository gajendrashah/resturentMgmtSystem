from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Table, Category, SubCategory, MenuItem, Building, Room, Customer, Cart, CartItem, Sale, Purchase, customerAdvance

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number',)
    search_fields = ('table_number',)
    list_per_page = 20

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    list_per_page = 20

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price')
    list_filter = ('subcategory__category', 'subcategory')
    search_fields = ('name', 'description')
    list_per_page = 20

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('building_name',)
    search_fields = ('building_name',)
    list_per_page = 20

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building')
    list_filter = ('building',)
    search_fields = ('room_number', 'building__building_name')
    list_per_page = 20

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'room')
    list_filter = ('room__building', 'room')
    search_fields = ('name', 'phone', 'email')
    list_per_page = 20

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'customer', 'created_at')
    list_filter = ('table', 'customer')
    search_fields = ('table__table_number', 'customer__name')
    list_per_page = 20
    inlines = [CartItemInline]

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'sale_date', 'status', 'print_sale')
    list_filter = ('status', 'sale_date')
    search_fields = ('cart__id', 'cart__customer__name', 'cart__table__table_number')
    actions = ['print_selected_sales']
    list_per_page = 20

    def print_sale(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Print</a>',
            reverse('print_sale', args=[obj.id])
        )
    print_sale.short_description = 'Print'
    print_sale.allow_tags = True

    def print_selected_sales(self, request, queryset):
        html = render_to_string('admin/sales/print_sales.html', {'sales': queryset})
        return HttpResponse(html)
    print_selected_sales.short_description = "Print selected sales"

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'total_cost', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('item_name', 'bill_number')
    list_per_page = 20
    
@admin.register(customerAdvance)
class CustomerAdvanceAdmin(admin.ModelAdmin):
    list_display = ('customers', 'Advance', 'Payment_Method')
    list_filter = ('Payment_Method',)
    search_fields = ('customers__name',)
    list_per_page = 20
