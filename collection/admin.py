from django.contrib import admin
from collection.models import Collections


class CollectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'signature', 'address_receiver', 'wallet', 'transaction')
    search_fields = ('id', 'type_transaction',)
    ordering = ('id',)

    fieldsets = (
        ('Transaction', {
            'fields': (
                ('id', 'name', 'signature', 'address_receiver', 'wallet', 'transaction', 'timestamp'),
            ),
        }),
    )


admin.site.register(Collections, CollectionsAdmin)
