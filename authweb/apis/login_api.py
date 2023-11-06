from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token
from utils.beez_crypto_utils import BeezCryptoUtils
from wallets.models import Wallet
from wallets.serializers import WalletSerializer


class APILogin(ObtainAuthToken):
    permission_classes = (AllowAny,)
    _error_credential = 'user_pass_not_valid'

    def post(self, request, format=None):
        email = request.data['email'].lower()
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is not None:
            if not check_password(password, user.password):
                raise exceptions.AuthenticationFailed({"success": False, "msg": self._error_credential})
            wallet = Wallet.objects.filter(user=user).first()
            serializer = WalletSerializer(wallet, many=False)
        else:
            passwd = make_password(password)
            user = User.objects.create(
                email=email,
                username=email,
                password=passwd,
                is_active=True
            )

            beez_obj = BeezCryptoUtils()
            beez_obj.generate_keys_from_mnemonic_words()
            mnemonic_words = beez_obj.get_words()
            private_key = beez_obj.get_private_key_str()
            public_key = beez_obj.get_public_key_str()
            address = beez_obj.generate_address(public_key)

            wallet = Wallet.objects.create(
                mnemonic=mnemonic_words,
                address=address,
                private_key=private_key,
                public_key=public_key,
                balance=0,
                user=user
            )

            serializer = WalletSerializer(wallet, many=False)

        token, created = Token.objects.get_or_create(user=user)
        content = {
            'access_token': str(token),
            'wallet': serializer.data
        }
        return JsonResponse(content)
