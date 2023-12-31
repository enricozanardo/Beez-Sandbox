from django.contrib import admin
from assets.models import Assets


class AssetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'signature', 'wallet', 'collections')
    search_fields = ('id',)
    ordering = ('name',)

    fieldsets = (
        ('Block', {
            'fields': (
                ('id', 'name', 'amount', 'file', 'wallet', 'collections', 'signature', 'timestamp'),
            ),
        }),
    )


admin.site.register(Assets, AssetsAdmin)
