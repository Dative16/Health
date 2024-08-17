from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, Patient, HealthCareProvider


class AdminAccount(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'gender', 'age', 'is_active', 'date_of_joined')
    list_display_links = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('date_of_birth',)
    ordering = ('-date_of_birth',)
    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'phone_number', 'age', 'gender',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('date_of_birth',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'password1', 'password2'),
        }),
    )


admin.site.register(Account, AdminAccount)
admin.site.register(Patient)
admin.site.register(HealthCareProvider)
