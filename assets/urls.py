from django.urls import path
from assets.apis import *

app_name = 'assets'

urlpatterns = [
    path('assets', ApiAssetsList.as_view(), name='api_list_assets'),
    path('ApiAssets', ApiAssets.as_view(), name='api_assets'),
    # path('collection/<collection_id>', ApiCollections.as_view(), name='api__collection'),
]
