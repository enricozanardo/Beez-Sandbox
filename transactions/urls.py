from django.urls import path
from transactions.apis import *

app_name = 'transaction'

urlpatterns = [
    path('transactions', ApiTransaction.as_view(), name='api_transactions'),
]
