from eventscanner.queue.pika_handler import send_to_backend
from mywish_models.models import Transfers, ExchangeRequests, session
from scanner.events.block_event import BlockEvent
from settings.settings_local import NETWORKS


class TransferMonitor:
    network_type = []
    currency = None
    event_type = 'transfer_confirm'

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_type:
            return

        tx_hashes = set()
        for address_transactions in block_event.transactions_by_address.values():
            for transaction in address_transactions:
                tx_hashes.add(transaction.tx_hash)

        transfers = session \
            .query(Transfers) \
            .filter(Transfers.tx_hash.in_(tx_hashes)) \
            .distinct(Transfers.tx_hash) \
            .all()
        for transfer in transfers:
            ID = [transfer.exchange_request_id,]
            print(ID)
            exchange_request = session.query(ExchangeRequests).filter(ExchangeRequests.id.in_(ID)).all()
            print(exchange_request)
            message = {
                'transactionHash': transfer.tx_hash,
                'userID': exchange_request[0].userID,
                'transferID': transfer.id,
                'amount': int(transfer.amount),
                'success': True,
                'status': 'COMMITTED',
            }
            send_to_backend(cls.event_type, NETWORKS[block_event.network.type]['queue'], message)


class DucxTransferMonitor(TransferMonitor):
    network_type = ['DUCATUSX_MAINNET']
    currency = 'DUCX'
