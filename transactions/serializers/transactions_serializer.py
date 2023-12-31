from rest_framework import serializers
from transactions.models import Transaction


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id", "type", "fee", "data", "address_sender", "address_receiver", "signature", "block_id",)
        depth = 1
