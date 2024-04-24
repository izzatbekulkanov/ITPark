from django.contrib import admin
from .models import Services, Queue, Icons

admin.site.register(Services)
@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'services', 'order_number', 'done', 'user')
    list_filter = ('services', 'done', 'user')
    search_fields = ('first_name', 'last_name', 'order_number')
    readonly_fields = ('order_number',)

class IconsAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at', 'updated_at')
    search_fields = ['name', 'icon']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Icons, IconsAdmin)