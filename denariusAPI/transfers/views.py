import datetime


from bitcoinrpc.authproxy import JSONRPCException
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
from denariusAPI.transfers.api import transfer_ducatus
from denariusAPI.bip32_ducatus import DucatusWallet


transfer_response = openapi.Response(
    description='Response with transfer info',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tx_hash': openapi.Schema(type=openapi.TYPE_STRING),
            'datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            'sender_address': openapi.Schema(type=openapi.TYPE_STRING),
            'receiver_address': openapi.Schema(type=openapi.TYPE_STRING),
            'transferred_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'number_of_confirmations': openapi.Schema(type=openapi.TYPE_NUMBER),
            'fee_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
},
    )
)



class TransferView(APIView):

    @swagger_auto_schema(
        operation_description="request to transfer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required = ['sender_address', 'receiver_address', 'DUC_amount'],
            properties = {
                'sender_address':openapi.Schema(type=openapi.TYPE_STRING),
                'receiver_address': openapi.Schema(type=openapi.TYPE_STRING),
                'DUC_amount': openapi.Schema(type=openapi.TYPE_NUMBER),

            },
        ),
        responses={200: transfer_response},
    )

    def post(self, request):
        request_data = request.data
        from_address = request_data.get('sender_address')
        to_address = request_data.get('receiver_address')
        amount = request_data.get('DUC_amount')
        try:
            transfer = transfer_ducatus(from_address, to_address, amount)
            response_data = {'tx_hash': transfer.tx_hash, 'sender_address': transfer.from_address, 'receiver_address': transfer.to_address,
                         'currency': 'DUC', 'transferred_amount': transfer.amount, 'fee_amount': transfer.transaction_fee,
                         'number of confirmations': transfer.number_of_confirmations, 'state': transfer.state,
                         'datetime': transfer.created_date.strftime("%m/%d/%Y, %H:%M:%S")}

        except JSONRPCException as e:
            print(e.message)
            if e.message == 'Amount out of range':
                response_data = {'Error': 'Invalid amount'}
            else:
                response_data = {'Error': 'Transfer failed'}
            
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)
