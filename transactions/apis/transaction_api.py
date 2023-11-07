from rest_framework import generics
from blocks.models import Block
from wallets.models import Wallet
from transactions.models import Transaction
from settings.enums import TypeTransfer as TypeTransferEnum
from settings.models import TypeTransfer
from blocks.serializers import BlockSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.beez_crypto_utils import BeezCryptoUtils
import json
import binascii
import hashlib
from datetime import datetime
from django.http import JsonResponse
import codecs

class ApiTransaction(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        wallet = Wallet.objects.filter(user=user).first()
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))
        data = request.data
        type_trans = str(data['type']).upper()
        type_transfer = TypeTransfer.objects.filter(key=type_trans).first()

        transaction_data = {
            "type_transaction": type_transfer.key,
            "fee": type_transfer.fee,
            "data": data['data'],
            "timestamp": timestamp,
            "token": data['token'],
            "address_receiver": data['address_receiver'],
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
            data=data['data'],
            token=data['token'],
            signature=signature_str,
            address_receiver=data['address_receiver'],
            address_sender=wallet.address,
            block_id=str(block.id),
            timestamp=timestamp
        )

        # INSERIRE I VARI CATCH CON LE COSE DA FARE

        content = {
            "id": transaction.id
        }

        return JsonResponse(content)
