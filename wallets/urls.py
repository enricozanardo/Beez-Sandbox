from django.urls import path
from wallets.apis import *

app_name = 'wallets'

urlpatterns = [
    path('wallets', ApiWallet.as_view(), name='detail_wallet'),
    path('wallet/transactions', ApiWalletTransactions.as_view(), name='list_transactions_from_wallet'),
]
