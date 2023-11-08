"""
URL configuration for beez_sandbox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.site.site_header = "Sandbox Beez"
admin.site.site_title = "Sandbox Beez"
admin.site.index_title = "Sandbox Beez"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('v1/', include([
            path('', include('authweb.urls', namespace="auth_api")),
            path('', include('blocks.urls', namespace="blocks_api")),
            path('', include('wallets.urls', namespace="wallet_api")),
            path('', include('transactions.urls', namespace="transaction_api")),
            path('', include('info.urls', namespace="info_api")),
            path('', include('assets.urls', namespace="assets_api")),
            path('', include('collection.urls', namespace="collection_api")),
        ])),
    ])),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
