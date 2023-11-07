from rest_framework import generics
from rest_framework.response import Response


class ApiInfo(generics.GenericAPIView):

    def get(self, request, format=None):
        response = "Blockchain!. 🦾 🐝 🐝 🐝 🦾"
        return Response(response)
