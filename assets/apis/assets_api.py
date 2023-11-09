from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallets.models import Wallet
from blocks.models import Block
from assets.models import Assets
from collection.models import Collections
from assets.serializers import AssetsSerializer, AllAssetsSerializer
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


class ApiAssetsList(generics.ListAPIView):
    queryset = Assets.objects.all().order_by('id')
    serializer_class = AllAssetsSerializer


class ApiMyAssetsList(generics.GenericAPIView):
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
        serialized = AssetsSerializer(assets, many=False)
        return Response(serialized.data)

    def post(self, request, format=None):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        data = request.data
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.CREATE_ASSET).first()

        if wallet.balance < type_transfer.fee:
            content = {
                "error": "balance can't be negative"
            }
            return JsonResponse(content, status=404)

        data_trans = hashlib.sha256(data['data'].encode('UTF-8'))

        transaction_data = {
            "type_transaction": TypeTransferEnum.CREATE_ASSET,
            "fee": type_transfer.fee,
            "data": str(data_trans.hexdigest()),
            "timestamp": timestamp,
            "address_receiver": wallet.address,
            "address_sender": wallet.address
        }

        beez_obj = BeezCryptoUtils()
        beez_obj.load_public_key(wallet.public_key)

        beez_obj.generate_keys_from_mnemonic_words(wallet.mnemonic)
        private_key = beez_obj.get_private_key_str()
        public_key = beez_obj.get_public_key_str()
        transaction_json = json.dumps(transaction_data)
        transaction_byte = str.encode(transaction_json)
        signature = beez_obj.generate_signature(transaction_byte)
        signature_str = binascii.hexlify(signature).decode("utf-8")
        transaction_id = hashlib.sha256(transaction_json.encode('UTF-8'))

        block_last = Block.objects.all().order_by('-block_count').first()
        count_block = 1
        last_hast = "Hello Beezkeepers! 🐝"

        if block_last:
            count_block = block_last.block_count + 1
            last_hast = block_last.id

        block_data = {
            "forger": wallet.address,
            "timestamp": timestamp,
            "count_block": count_block,
            "last_hash": last_hast
        }
        block_json = json.dumps(block_data)
        block_byte = str.encode(block_json)
        signature_block = beez_obj.generate_signature(block_byte)
        signature_block_str = binascii.hexlify(signature_block).decode("utf-8")
        block_id = hashlib.sha256(block_json.encode('UTF-8'))

        block = Block.objects.create(
            id=str(block_id.hexdigest()),
            forger=wallet.address,
            timestamp=timestamp,
            block_count=count_block,
            last_hash=last_hast,
            signature=signature_block_str
        )

        transaction = Transaction.objects.create(
            id=str(transaction_id.hexdigest()),
            type_transaction_id=str(type_transfer.key),
            fee=type_transfer.fee,
            data=str(data_trans.hexdigest()),
            signature=signature_str,
            address_receiver=wallet.address,
            address_sender=wallet.address,
            block_id=str(block.id),
            timestamp=timestamp
        )

        asset_data = {
            "name": data['name'],
            "file": data['data'],
            "timestamp": timestamp,
            "wallet_id": wallet.id,
            "transaction_id": transaction.id,
            "collection": None
        }

        asset_json = json.dumps(asset_data)
        asset_byte = str.encode(asset_json)
        signature_asset = beez_obj.generate_signature(asset_byte)
        asset_collection_str = binascii.hexlify(signature_asset).decode("utf-8")
        asset_id = hashlib.sha256(asset_json.encode('UTF-8'))

        assets_obj = Assets.objects.create(
            id=str(asset_id.hexdigest()),
            timestamp=timestamp,
            signature=signature_str,
            name=data['name'],
            amount=data['amount'],
            file=data['data'],
            wallet_id=wallet.id
        )

        decrease = type_transfer.fee
        current_amount = wallet.balance
        new_current_amount = current_amount - decrease
        wallet.balance = new_current_amount
        wallet.save()

        content = {
            "id": assets_obj.id
        }

        return JsonResponse(content)


class ApiMoveAssets(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, assets_id, format=None):
        user = self.request.user
        data = request.data
        wallet = Wallet.objects.filter(user=user).first()
        assets = Assets.objects.filter(id=assets_id, wallet_id=wallet.id).first()

        type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.UPDATE_ASSET).first()

        if wallet.balance < type_transfer.fee:
            content = {
                "error": "balance can't be negative"
            }
            return JsonResponse(content, status=404)

        if assets is None:
            content = {
                "error": "asset not found"
            }
            return JsonResponse(content, status=404)

        if data['collection_id'] is not None:
            collection = Collections.objects.filter(id=data['collection_id'], wallet_id=wallet.id).first()

            if collection is None:
                content = {
                    "error": "collection not found"
                }
                return JsonResponse(content, status=404)

        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        data_trans = data['collection_id']
        if data_trans is None:
            data_trans = 'empty'

        transaction_data = {
            "type_transaction": TypeTransferEnum.UPDATE_ASSET,
            "fee": type_transfer.fee,
            "data": data_trans,
            "timestamp": timestamp,
            "address_receiver": wallet.address,
            "address_sender": wallet.address
        }

        beez_obj = BeezCryptoUtils()
        beez_obj.load_public_key(wallet.public_key)

        beez_obj.generate_keys_from_mnemonic_words(wallet.mnemonic)
        private_key = beez_obj.get_private_key_str()
        public_key = beez_obj.get_public_key_str()
        transaction_json = json.dumps(transaction_data)
        transaction_byte = str.encode(transaction_json)
        signature = beez_obj.generate_signature(transaction_byte)
        signature_str = binascii.hexlify(signature).decode("utf-8")
        transaction_id = hashlib.sha256(transaction_json.encode('UTF-8'))

        block_last = Block.objects.all().order_by('-block_count').first()
        count_block = 1
        last_hast = "Hello Beezkeepers! 🐝"

        if block_last:
            count_block = block_last.block_count + 1
            last_hast = block_last.id

        block_data = {
            "forger": wallet.address,
            "timestamp": timestamp,
            "count_block": count_block,
            "last_hash": last_hast
        }
        block_json = json.dumps(block_data)
        block_byte = str.encode(block_json)
        signature_block = beez_obj.generate_signature(block_byte)
        signature_block_str = binascii.hexlify(signature_block).decode("utf-8")
        block_id = hashlib.sha256(block_json.encode('UTF-8'))

        block = Block.objects.create(
            id=str(block_id.hexdigest()),
            forger=wallet.address,
            timestamp=timestamp,
            block_count=count_block,
            last_hash=last_hast,
            signature=signature_block_str
        )

        transaction = Transaction.objects.create(
            id=str(transaction_id.hexdigest()),
            type_transaction_id=str(type_transfer.key),
            fee=type_transfer.fee,
            data=data_trans,
            signature=signature_str,
            address_receiver=wallet.address,
            address_sender=wallet.address,
            block_id=str(block.id),
            timestamp=timestamp
        )

        assets.collections_id = data['collection_id']
        assets.save()

        decrease = type_transfer.fee
        current_amount = wallet.balance
        new_current_amount = current_amount - decrease
        wallet.balance = new_current_amount
        wallet.save()

        content = {
            "id": assets.id,
            "success": True
        }

        return JsonResponse(content)


class ApiTransferAssets(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        data = request.data
        wallet = Wallet.objects.filter(user=user).first()
        assets = Assets.objects.filter(id=data['assets_id']).first()

        if assets is None:
            content = {
                "error": "asset not found"
            }
            return JsonResponse(content, status=404)

        type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.UPDATE_ASSET).first()
        cost = type_transfer.fee + assets.amount
        if wallet.balance < cost:
            content = {
                "error": "balance can't be negative"
            }
            return JsonResponse(content, status=404)

        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        transaction_data = {
            "type_transaction": TypeTransferEnum.UPDATE_ASSET,
            "fee": type_transfer.fee,
            "data": data['assets_id'],
            "timestamp": timestamp,
            "address_receiver": wallet.address,
            "address_sender": assets.address
        }

        beez_obj = BeezCryptoUtils()
        beez_obj.load_public_key(wallet.public_key)

        beez_obj.generate_keys_from_mnemonic_words(wallet.mnemonic)
        private_key = beez_obj.get_private_key_str()
        public_key = beez_obj.get_public_key_str()
        transaction_json = json.dumps(transaction_data)
        transaction_byte = str.encode(transaction_json)
        signature = beez_obj.generate_signature(transaction_byte)
        signature_str = binascii.hexlify(signature).decode("utf-8")
        transaction_id = hashlib.sha256(transaction_json.encode('UTF-8'))

        block_last = Block.objects.all().order_by('-block_count').first()
        count_block = 1
        last_hast = "Hello Beezkeepers! 🐝"

        if block_last:
            count_block = block_last.block_count + 1
            last_hast = block_last.id

        block_data = {
            "forger": wallet.address,
            "timestamp": timestamp,
            "count_block": count_block,
            "last_hash": last_hast
        }
        block_json = json.dumps(block_data)
        block_byte = str.encode(block_json)
        signature_block = beez_obj.generate_signature(block_byte)
        signature_block_str = binascii.hexlify(signature_block).decode("utf-8")
        block_id = hashlib.sha256(block_json.encode('UTF-8'))

        block = Block.objects.create(
            id=str(block_id.hexdigest()),
            forger=wallet.address,
            timestamp=timestamp,
            block_count=count_block,
            last_hash=last_hast,
            signature=signature_block_str
        )

        transaction = Transaction.objects.create(
            id=str(transaction_id.hexdigest()),
            type_transaction_id=str(type_transfer.key),
            fee=type_transfer.fee,
            data=data['assets_id'],
            signature=signature_str,
            address_receiver=wallet.address,
            address_sender=wallet.address,
            block_id=str(block.id),
            timestamp=timestamp
        )

        old_owner = Wallet.objects.filter(id=assets.wallet_id).first()
        current_balance = old_owner.balance
        current_balance = current_balance + assets.amount
        old_owner.balance = current_balance
        old_owner.save()

        assets.collections_id = None
        assets.wallet_id = wallet.id
        assets.save()

        decrease = type_transfer.fee + assets.amount
        current_amount = wallet.balance
        new_current_amount = current_amount - decrease
        wallet.balance = new_current_amount
        wallet.save()

        content = {
            "id": assets.id,
            "success": True
        }

        return JsonResponse(content)
