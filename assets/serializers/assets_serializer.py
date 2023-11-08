from rest_framework import serializers
from assets.models import Assets


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = (
            "id", "name", "file", "signature", "wallet", "collections", "timestamp")
        depth = 1
