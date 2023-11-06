from rest_framework import serializers
from blocks.models import Block


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = "__all__"
        depth = 2
