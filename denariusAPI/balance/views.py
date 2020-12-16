import datetime
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from denariusAPI.settings import NETWORK_SETTINGS
from denariusAPI.exchange_requests.models import DucatusUser
from denariusAPI.bip32_ducatus import DucatusWallet


balance_response = openapi.Response(
    description='Response with balance',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'amount': openapi.Schema(type=openapi.TYPE_STRING)
},
    )
)

class BalanceView(APIView):

    @swagger_auto_schema(
        operation_description="request to get balance",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required='address',
            properties={'address': openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        responses={200: balance_response},

    )
    def post(self, request):
        request_data = request.data
        address = request_data.get('address')
        balance = requests.get(f'https://ducapi.rocknblock.io/api/DUC/mainnet/address/{address}/balance')
        balance = balance.json()
        response_data = {'amount': balance['balance'], 'currency': 'DUC'}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)


def create_ducatus_user():
    ducatus_user = DucatusUser()
    ducatus_user.generate_keys()
    ducatus_user.save()
    print('address', ducatus_user.__dict__, flush=True)

    return ducatus_user