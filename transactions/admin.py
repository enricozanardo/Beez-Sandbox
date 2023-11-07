from django.contrib import admin
from transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_transaction', 'address_sender', 'address_receiver', 'block')
    search_fields = ('id', 'type_transaction', )
    ordering = ('id',)

    fieldsets = (
        ('Transaction', {
            'fields': (
                ('id', 'type_transaction', 'fee', 'address_sender', 'address_receiver', 'block', 'signature', 'token', 'timestamp'),
            ),
        }),
    )

admin.site.register(Transaction, TransactionAdmin)
