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
from denariusAPI.transfers.models import DucatusTransfer
from denariusAPI.history.api import get_transactions

history_response = openapi.Response(
    description='Response with transfer history',
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT,
        properties={'txs':openapi.Schema(type=openapi.TYPE_OBJECT, properties={'tx_hash': openapi.Schema(type=openapi.TYPE_STRING),
            'datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            'sender_address': openapi.Schema(type=openapi.TYPE_STRING),
            'receiver_address': openapi.Schema(type=openapi.TYPE_STRING),
            'transferred_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'number_of_confirmations': openapi.Schema(type=openapi.TYPE_NUMBER),
            'fee_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'state': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),},)
    )
)


class HistoryView(APIView):

    @swagger_auto_schema(
        operation_description="request to get transfer history",
        responses={200: history_response},
    )

    def get(self, request, address):
        transaction_list = get_transactions(address)
        response_data = {'txs': transaction_list}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)



transaction_response = openapi.Response(
    description='Response with transaction',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'tx_hash': openapi.Schema(type=openapi.TYPE_STRING),
            'datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            'sender_address': openapi.Schema(type=openapi.TYPE_STRING),
            'receiver_address': openapi.Schema(type=openapi.TYPE_STRING),
            'transferred_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'number_of_confirmations': openapi.Schema(type=openapi.TYPE_NUMBER),
            'fee_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'state': openapi.Schema(type=openapi.TYPE_STRING)
                }
    )
)


class TransactionView(APIView):

    @swagger_auto_schema(
        operation_description="request to get transaction",
        responses={200: transaction_response},
    )

    def get(self, request, tx_hash):
        transfer = DucatusTransfer.objects.filter(tx_hash=tx_hash).last()
        response_data = {'tx_hash': transfer.tx_hash, 'sender_address': transfer.from_address, 'receiver_address': transfer.to_address,
                         'currency': 'DUC', 'transferred_amount': transfer.amount, 'fee_amount': transfer.transaction_fee,
                         'number of confirmations': transfer.number_of_confirmations, 'state': transfer.state,
                         'datetime': transfer.created_date.strftime("%m/%d/%Y, %H:%M:%S")}

        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)




