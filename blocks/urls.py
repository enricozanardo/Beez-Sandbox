from django.urls import path
from blocks.apis import *

app_name = 'blocks'

urlpatterns = [
    path('blocks', ApiListBlocks.as_view(), name='list_blocks'),
    path('blocks/<block_id>', ApiDetailsBlock.as_view(), name='detail_block'),
]
