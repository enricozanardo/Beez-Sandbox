from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallets.models import Wallet
from blocks.models import Block
from collection.models import Collections
from collection.serializers import CollectionsSerializer
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


class ApiCollectionList(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        collections = Collections.objects.filter(wallet_id=wallet.id)
        serialized = CollectionsSerializer(collections, many=True)
        return Response(serialized.data)


class ApiCollectionDelete(generics.DestroyAPIView):
    queryset = Collections.objects.all()
    serializer_class = CollectionsSerializer


class ApiCollections(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, collection_id, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        collection = Collections.objects.filter(id=collection_id, wallet_id=wallet.id).first()
        if collection is None:
            content = {
                "error": "collection not found"
            }
            return JsonResponse(content, status=404)

        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.DELETE_COLLECTION).first()
        transaction_data = {
            "type_transaction": TypeTransferEnum.DELETE_COLLECTION,
            "fee": type_transfer.fee,
            "data": collection_id,
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
            data=collection_id,
            signature=signature_str,
            address_receiver=wallet.address,
            address_sender=wallet.address,
            block_id=str(block.id),
            timestamp=timestamp
        )

        collection.delete()

        decrease = type_transfer.fee
        current_amount = wallet.balance
        new_current_amount = current_amount - decrease
        wallet.balance = new_current_amount
        wallet.save()

        content = {
            "id": collection_id,
            "success": True
        }
        return JsonResponse(content)

    def get(self, request, collection_id, *args, **kwargs):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        collection = Collections.objects.filter(id=collection_id, wallet_id=wallet.id).first()
        if collection is None:
            content = {
                "error": "collection not found"
            }
            return JsonResponse(content, status=404)
        serialized = CollectionsSerializer(collection, many=False)
        return Response(serialized.data)

    def put(self, request, collection_id, format=None):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        data = request.data
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        collection = Collections.objects.filter(id=collection_id, wallet_id=wallet.id).first()
        if collection:
            type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.UPDATE_COLLECTION).first()
            transaction_data = {
                "type_transaction": TypeTransferEnum.UPDATE_COLLECTION,
                "fee": type_transfer.fee,
                "data": data['name'],
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
                data=data['name'],
                signature=signature_str,
                address_receiver=wallet.address,
                address_sender=wallet.address,
                block_id=str(block.id),
                timestamp=timestamp
            )

            collection.name = data['name']
            collection.save()

            decrease = type_transfer.fee
            current_amount = wallet.balance
            new_current_amount = current_amount - decrease
            wallet.balance = new_current_amount
            wallet.save()

            content = {
                "id": collection.id,
                "success": True
            }
            return JsonResponse(content)
        else:
            content = {
                "error": "collection not found"
            }
            return JsonResponse(content, status=404)

    def post(self, request, format=None):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        data = request.data
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        type_transfer = TypeTransfer.objects.filter(key=TypeTransferEnum.CREATE_COLLECTION).first()

        transaction_data = {
            "type_transaction": TypeTransferEnum.CREATE_COLLECTION,
            "fee": type_transfer.fee,
            "data": data['name'],
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
            data=data['name'],
            signature=signature_str,
            address_receiver=wallet.address,
            address_sender=wallet.address,
            block_id=str(block.id),
            timestamp=timestamp
        )

        collection_data = {
            "name": data['name'],
            "timestamp": timestamp,
            "wallet_id": wallet.id,
            "transaction_id": transaction.id
        }

        collection_json = json.dumps(collection_data)
        collection_byte = str.encode(collection_json)
        signature_collection = beez_obj.generate_signature(collection_byte)
        signature_collection_str = binascii.hexlify(signature_collection).decode("utf-8")
        collection_id = hashlib.sha256(collection_json.encode('UTF-8'))

        collection = Collections.objects.create(
            id=str(collection_id.hexdigest()),
            timestamp=timestamp,
            signature=signature_str,
            name=data['name'],
            wallet_id=wallet.id,
            transaction_id=transaction.id
        )

        decrease = type_transfer.fee
        current_amount = wallet.balance
        new_current_amount = current_amount - decrease
        wallet.balance = new_current_amount
        wallet.save()

        content = {
            "id": collection.id
        }

        return JsonResponse(content)
