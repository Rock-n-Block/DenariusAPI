import sys
import traceback
import requests
from decimal import Decimal
from rest_framework_api_key.models import APIKey

from denariusAPI.transfers.models import DucatusTransfer
from denariusAPI.exchange_requests.models import DucatusUser
from denariusAPI.settings import ROOT_KEYS
from denariusAPI.exchange_requests.models import DucatusUser
from denariusAPI.consts import DECIMALS
from bip32utils import BIP32Key
from denariusAPI.Bitcoin_api import BitcoinRPC, BitcoinAPI
from denariusAPI.bip32_ducatus import DucatusWallet

class TransferException(Exception):
    pass


def transfer_ducatus(from_address, to_address, amount):
    print('ducatus transfer started: sending {amount} DUC to {addr}'.format(amount=amount, addr=to_address), flush=True)
    currency = 'DUC'

    root_wallet = DucatusWallet.from_master_secret(network='ducatus', seed=ROOT_KEYS['ducatus']['seed'])
    child = DucatusUser.objects.get(address=from_address)
    child_wallet = root_wallet.get_child(child.id, is_prime=False, as_private=True)
    priv_key = child_wallet.export_to_wif().decode("utf-8")

    api = BitcoinAPI()
    inputs, value, response_ok = api.get_address_unspent_all(from_address)

    if not response_ok:
        print(f'Failed to fetch information about BTC address {from_address}', flush=True)
        return

    balance = int(value)
    if balance <= 0:
        balance = 0

    rpc = BitcoinRPC()
    transaction_fee = rpc.relay_fee
    if balance < transaction_fee + int(amount):
        print('balance is too low to send', flush=True)

    send_amount = int(amount) / DECIMALS['DUC']

    output_params = {to_address: send_amount, from_address:balance/ DECIMALS['DUC']-send_amount-transaction_fee/ DECIMALS['DUC']}
    print(f'send tx params: from {from_address} to {to_address} on amount {send_amount}', flush=True)
    sent_tx_hash = rpc.construct_and_send_tx(inputs, output_params, priv_key)
    print(sent_tx_hash)
    if not sent_tx_hash:
        err_str = f'Withdraw failed for address {from_address} and amount {send_amount} ({balance} - {transaction_fee})'
        print(err_str, flush=True)

    transfer = save_transfer(from_address, sent_tx_hash, amount, currency, to_address, transaction_fee)

    print('ducatus transfer ok', flush=True)
    return transfer


def save_transfer(from_address, tx, amount, currency, to_address, transaction_fee):
    ducatus_user = DucatusUser.objects.get(address = from_address)
    transfer = DucatusTransfer(
        ducatus_user = ducatus_user,
        tx_hash = tx,
        from_address = from_address,
        to_address = to_address,
        amount = amount,
        currency = currency,
        transaction_fee = transaction_fee,
        state = 'WAITING_FOR_CONFIRMATION',
    )
    transfer.save()

    print('transfer saved', flush=True)
    return transfer


def confirm_transfer(message):
    transfer_id = message['transferID']
    # transfer_address = message['address']
    transfer = DucatusTransfer.objects.get(id=transfer_id, state='WAITING_FOR_CONFIRMATION')
    print('transfer id {id} address {addr} '.format(id=transfer_id, addr=transfer.ducatus_user.address),
          flush=True)
    # if transfer_address == transfer.request.duc_address:
    transfer.state = 'DONE'
    transfer.number_of_confirmations = message['confirmations']
    transfer.save()
    requests.post(url = 'https://prod-11.westeurope.logic.azure.com/workflows/ac0f72b72d4d48508f2b2a2a2693d1f6/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ohdW3-hM7xDJUxIjx-8VdDOgQ-_ut06IUYG4awAjxwk', 
    data = {'tx_hash':transfer.tx_hash}, headers={"x-api-key" : 'https://prod-11.westeurope.logic.azure.com/workflows/ac0f72b72d4d48508f2b2a2a2693d1f6/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ohdW3-hM7xDJUxIjx-8VdDOgQ-_ut06IUYG4awAjxwk'}
    )
    print('transfer completed ok')
    return


def parse_payment_message(message):
    tx = message.get('transactionHash')

    if not DucatusTransfer.objects.filter(tx_hash=tx).count() > 0:
        ducatus_user = message.get('ducatus_user')
        ducatus_user = DucatusUser.objects.get(id=ducatus_user)
        amount = message.get('amount')
        currency = message.get('currency')
        to_address = message.get('to_address')
        state=message.get('status')
        number_of_confirmations = message.get('confirmations')

        transfer = DucatusTransfer(
            ducatus_user = ducatus_user,
            tx_hash = tx,
            to_address = to_address,
            amount = amount,
            currency = currency,
            state = state,
            number_of_confirmations = number_of_confirmations
        )
        transfer.save()
        requests.post(url = 'https://prod-11.westeurope.logic.azure.com/workflows/ac0f72b72d4d48508f2b2a2a2693d1f6/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ohdW3-hM7xDJUxIjx-8VdDOgQ-_ut06IUYG4awAjxwk',
        data = {'tx_hash':transfer.tx_hash}, headers={"x-api-key" : 'https://prod-11.westeurope.logic.azure.com/workflows/ac0f72b72d4d48508f2b2a2a2693d1f6/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ohdW3-hM7xDJUxIjx-8VdDOgQ-_ut06IUYG4awAjxwk'}
        )

        print(f'PAYMENT: {amount} {currency} to user {ducatus_user.id} with hash {tx}', flush=True)
