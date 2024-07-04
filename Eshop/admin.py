from django.contrib import admin
from .models import Category, Book
from.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'quantity', 'get_categories')

    def get_categories(self, obj):
        return ", ".join([category.category_name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'


admin.site.register(Book, BookAdmin)

from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)


 
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_order_id', 'user', 'payment_status', 'order_date')
    list_filter = ('payment_status', 'order_date')
    search_fields = ('user__username', 'get_order_id')
    readonly_fields = ('get_order_id',)

    def get_order_id(self, obj):
        return obj.get_order_id()
    get_order_id.short_description = 'Order ID'

admin.site.register(Order, OrderAdmin)


from .models import BookRequest

class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'book', 'pickup_location', 'seller_profile', 'status')
    list_filter = ('seller_profile', 'pickup_location', 'status')
    search_fields = ('full_name', 'email', 'pickup_location')
    list_per_page = 20
    fieldsets = (
        ('Request Information', {
            'fields': ('full_name', 'email', 'address', 'phone_number', 'pickup_location', 'status')
        }),
        ('Book Information', {
            'fields': ('book', 'seller_profile')
        }),
    )
    readonly_fields = ('full_name', 'email', 'address', 'phone_number', 'pickup_location', 'book', 'seller_profile')

admin.site.register(BookRequest, BookRequestAdmin)


from django.contrib import admin
from .models import Membership

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('plan', 'status', 'profile')
    list_filter = ('plan', 'status')
    search_fields = ('plan', 'status')
    list_per_page = 20

admin.site.register(Membership, MembershipAdmin)


admin.site.register(OrderItem)