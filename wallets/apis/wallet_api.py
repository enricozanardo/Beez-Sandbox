from rest_framework import generics
from wallets.models import Wallet
from wallets.serializers import WalletSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionsSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Q


class ApiWallet(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        serializer = WalletSerializer(wallet, many=False)
        return JsonResponse(serializer.data)


class ApiWalletTransactions(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        transactions = Transaction.objects.filter(
            Q(address_sender=wallet.address) | Q(address_receiver=wallet.address)).order_by('timestamp')
        serializer = TransactionsSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)
