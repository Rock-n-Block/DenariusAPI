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
from denariusAPI.transfers.api import transfer_ducatus, get_transactions
from denariusAPI.bip32_ducatus import DucatusWallet


transfer_response = openapi.Response(
    description='Response with transfer info',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tx_hash': openapi.Schema(type=openapi.TYPE_STRING),
            'datetime': openapi.Schema(type=openapi.TYPE_STRING),
            'sender address': openapi.Schema(type=openapi.TYPE_STRING),
            'receiver address': openapi.Schema(type=openapi.TYPE_STRING),
            'transferred amount': openapi.Schema(type=openapi.TYPE_STRING),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'number of confirmations': openapi.Schema(type=openapi.TYPE_STRING),
            'fee amount': openapi.Schema(type=openapi.TYPE_STRING),
},
    )
)

history_response = openapi.Response(
    description='Response with transfer history',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'txs':openapi.Schema(type=openapi.TYPE_STRING),},
    )
)



class TransferView(APIView):

    @swagger_auto_schema(
        operation_description="request to transfer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required = ['sender address', 'receiver address', 'DUC amount'],
            properties = {
                'sender address':openapi.Schema(type=openapi.TYPE_STRING),
                'receiver address': openapi.Schema(type=openapi.TYPE_STRING),
                'DUC amount': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
        responses={200: transfer_response},
    )

    def post(self, request):
        request_data = request.data
        from_address = request_data.get('sender address')
        to_address = request_data.get('receiver address')
        amount = request_data.get('DUC amount')
        transfer = transfer_ducatus(from_address, to_address, amount)
        response_data = {'tx_hash': transfer.tx_hash, 'sender_address': transfer.from_address, 'receiver_address': transfer.to_address,
                         'currency': 'DUC', 'transferred_amount': transfer.amount, 'fee_amount': transfer.transaction_fee,
                         'number of confirmations': transfer.number_of_confirmations, 'state': transfer.state,
                         'datetime': transfer.created_date.strftime("%m/%d/%Y, %H:%M:%S")}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)


class HistoryView(APIView):

    @swagger_auto_schema(
        operation_description="request to get transfer history",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required = ['wallet address'],
            properties = {
                'wallet address':openapi.Schema(type=openapi.TYPE_STRING),
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