from django.contrib import admin
from wallets.models import Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ('address', 'public_key', 'balance', 'user')
    search_fields = ('address',)
    ordering = ('address',)

    fieldsets = (
        ('Wallet', {
            'fields': (
                ('mnemonic', 'address', 'private_key', 'public_key', 'balance', 'user', 'called_exchange'),
            ),
        }),
    )


admin.site.register(Wallet, WalletAdmin)
