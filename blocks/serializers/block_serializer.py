from rest_framework import serializers
from blocks.models import Block


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("id", "block_count", "forger", "last_hash", "signature", "timestamp", "transactions",)
        depth = 2
