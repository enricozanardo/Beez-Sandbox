from django.urls import path
from transactions.apis import *

app_name = 'transaction'

urlpatterns = [
    path('transactions', ApiListTransactions.as_view(), name='api_list_transactions'),
    path('transaction', ApiTransaction.as_view(), name='api_create_transactions'),
    path('transaction/<transaction_id>', ApiTransactionDetails.as_view(), name='api_deatil_transaction'),
]
