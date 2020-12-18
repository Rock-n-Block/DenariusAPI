import datetime

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
from denariusAPI.history.api import get_transactions

history_response = openapi.Response(
    description='Response with transfer history',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'txs':openapi.Schema(type=openapi.TYPE_STRING),},
    )
)


class HistoryView(APIView):

    @swagger_auto_schema(
        operation_description="request to get transfer history",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required = ['wallet_address'],
            properties = {
                'wallet_address':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: history_response},
    )

    def post(self, request):
        request_data = request.data
        address = request_data.get('wallet address')
        transaction_list = get_transactions(address)
        response_data = {'txs': transaction_list}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)





