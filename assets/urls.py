from django.urls import path
from assets.apis import *

app_name = 'assets'

urlpatterns = [
    path('my-assets', ApiMyAssetsList.as_view(), name='api_my_list_assets'),
    path('assets', ApiAssetsList.as_view(), name='api_list_assets'),
    path('asset/transfer', ApiTransferAssets.as_view(), name='api_asset_transfer'),
    path('asset', ApiAssets.as_view(), name='api_assets'),
    path('asset/<assets_id>', ApiAssets.as_view(), name='api_assets_details'),
    path('asset/move/<assets_id>', ApiMoveAssets.as_view(), name='api_assets_move_collection'),
]
