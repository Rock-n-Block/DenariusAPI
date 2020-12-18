from denariusAPI.transfers.models import DucatusTransfer
from denariusAPI.exchange_requests.models import DucatusUser

def get_transactions(address):
    transaction_list = []
    ducatus_user = DucatusUser.objects.get(address = address)
    transfers = DucatusTransfer.objects.filter(ducatus_user = ducatus_user)
    for transfer in transfers:
        transaction_list.append({'tx_hash': transfer.tx_hash, 'sender_address': transfer.from_address, 'receiver_address': transfer.to_address,
                         'currency': 'DUC', 'transferred_amount': transfer.amount, 'fee_amount': transfer.transaction_fee,
                         'number_of_confirmations': transfer.number_of_confirmations, 'state': transfer.state,
                         'datetime': transfer.created_date.strftime("%m/%d/%Y, %H:%M:%S")})
    print(f'transaction_list: {transaction_list}')
    return transaction_list

