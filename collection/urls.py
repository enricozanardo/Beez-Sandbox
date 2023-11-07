from django.urls import path
from collection.apis import *

app_name = 'collection'

urlpatterns = [
    path('collections', ApiCollectionList.as_view(), name='api_list_collection'),
    path('collection', ApiCollections.as_view(), name='api_create_collection'),
    path('collection/<collection_id>', ApiCollections.as_view(), name='api__collection'),
]
