import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from denariusAPI.exchange_requests.models import DucatusUser
from denariusAPI.bip32_ducatus import DucatusWallet
from denariusAPI.transfers.serializers import DucatusTransferSerializer


exchange_response = openapi.Response(
    description='Response with DUC address',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'duc_address': openapi.Schema(type=openapi.TYPE_STRING)
},
    )
)

class ExchangeRequestView(APIView):

    @swagger_auto_schema(
        operation_description="request to create DUC address",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
        ),
        responses={200: exchange_response},

    )
    def post(self, request):
        ducatus_user = create_ducatus_user()
        response_data = {'duc_address': ducatus_user.address}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)


def create_ducatus_user():
    ducatus_user = DucatusUser()
    ducatus_user.save()
    ducatus_user.generate_keys()
    ducatus_user.save()
    print('address', ducatus_user.__dict__, flush=True)

    return ducatus_user