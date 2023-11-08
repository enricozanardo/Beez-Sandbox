from rest_framework import serializers
from assets.models import Assets


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = (
            "id", "name", "file", "amount", "signature", "address", "collections_id", "timestamp")
        depth = 1


class AllAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = (
            "id", "name", "amount", "signature", "address")
        depth = 1
