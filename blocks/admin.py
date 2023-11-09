from django.contrib import admin
from blocks.models import Block


class BlocksAdmin(admin.ModelAdmin):
    list_display = ('id', 'block_count', 'forger', 'last_hash',)
    search_fields = ('id',)
    ordering = ('block_count',)

    fieldsets = (
        ('Block', {
            'fields': (
                ('id', 'block_count', 'forger', 'signature', 'last_hash', 'timestamp'),
            ),
        }),
    )


admin.site.register(Block, BlocksAdmin)
