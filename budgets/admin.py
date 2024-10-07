from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'request_date']
    list_display_links = ['id', 'user']
    list_per_page = 10
    ordering = ['request_date',]
    list_filter = ['status',]
    readonly_fields = [
        'request_date',
        'contacted_date'
    ]
    list_filter = ['status', 'request_date']
