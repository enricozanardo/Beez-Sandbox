from rest_framework import serializers
from collection.models import Collections


class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = (
            "id", "name", "signature", "address", "transaction_id", "timestamp",)
        depth = 1
