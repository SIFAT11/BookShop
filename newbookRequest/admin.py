from django.contrib import admin
from .models import newbookRequest

@admin.register(newbookRequest)
class newbookRequestAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'writter_name', 'publication', 'edition', 'request_date', 'phone_number', 'email')
    search_fields = ('book_name', 'writter_name', 'publication', 'edition', 'phone_number', 'email')
    list_filter = ('request_date',)
