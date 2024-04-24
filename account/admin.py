from django.contrib import admin

from account.models import CustomUser


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active', 'is_superuser')  # qaysi qatorlar chiqishini ko'rsatish
    list_filter = ('is_staff', 'is_active')  # chiqishni filterlash
    search_fields = ('username', 'email', 'full_name')  # qidirish maydonlarini tanlash
    ordering = ('-date_joined',)  # Tartiblash
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)