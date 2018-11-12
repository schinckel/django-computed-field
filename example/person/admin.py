from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'active',
        'first_name', 'last_name',
    )

    search_fields = ('name',)
    readonly_fields = ('name',)
    list_filter = ('active', 'name')
