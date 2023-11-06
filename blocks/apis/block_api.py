from rest_framework import generics
from blocks.models import Block
from blocks.serializers import BlockSerializer
from rest_framework.response import Response


class ApiListBlocks(generics.ListAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ApiDetailsBlock(generics.GenericAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    def get(self, request, block_id, *args, **kwargs):
        block = Block.objects.filter(id=block_id).first()
        serialized = BlockSerializer(block, many=False)
        return Response(serialized.data)
