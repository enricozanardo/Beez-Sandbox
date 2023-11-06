from rest_framework import generics
from wallets.models import Wallet
from wallets.serializers import WalletSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


class ApiWallet(generics.GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        serializer = WalletSerializer(wallet, many=False)
        content = {
            'access_token': user.email,
        }
        return JsonResponse(serializer.data)
