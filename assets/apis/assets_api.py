from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallets.models import Wallet
from blocks.models import Block
from assets.models import Assets
from collection.models import Collections
from assets.serializers import AssetsSerializer
from utils.beez_crypto_utils import BeezCryptoUtils
from transactions.models import Transaction
import json
import binascii
import hashlib
from datetime import datetime
from settings.enums import TypeTransfer as TypeTransferEnum
from settings.models import TypeTransfer
from django.http import JsonResponse
from rest_framework.response import Response


class ApiAssetsList(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        assets = Assets.objects.filter(wallet_id=wallet.id)
        serialized = AssetsSerializer(assets, many=True)
        return Response(serialized.data)


class ApiAssets(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, assets_id, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        assets = Assets.objects.filter(id=assets_id, wallet_id=wallet.id).first()
        if assets is None:
            content = {
                "error": "asset not found"
            }
            return JsonResponse(content, status=404)
        serialized = AssetsSerializer(collection, many=False)
        return Response(serialized.data)

    def post(self, request, format=None):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        data = request.data
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.CREATE_COLLECTION).first()

