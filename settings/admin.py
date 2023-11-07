from django.contrib import admin
from settings.models import TypeTransfer


class TypeTransferAdmin(admin.ModelAdmin):
    list_display = ('key', 'description', 'fee')
    search_fields = ('key',)
    ordering = ('key',)

    fieldsets = (
        ('Type Transfer', {
            'fields': (
                ('key', 'fee', 'description',),
            ),
        }),
    )


admin.site.register(TypeTransfer, TypeTransferAdmin)
