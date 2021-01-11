from eventscanner.queue.pika_handler import send_to_backend
from mywish_models.models import Transfers, DucatusUser, session
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
                confirmations = transaction.inputs
                tx_hashes.add(transaction.tx_hash)
        transfers = session \
            .query(Transfers) \
            .filter(Transfers.tx_hash.in_(tx_hashes)) \
            .distinct(Transfers.tx_hash) \
            .all()
        for transfer in transfers:
            ID = [transfer.ducatus_user_id,]
            print(ID)
            ducatus_user = session.query(DucatusUser).filter(DucatusUser.id.in_(ID)).all()
            print(ducatus_user)
            message = {
                'transactionHash': transfer.tx_hash,
                'ducatus_user': ducatus_user[0].id,
                'transferID': transfer.id,
                'confirmations': confirmations,
                'amount': int(transfer.amount),
                'success': True,
                'status': 'COMMITTED',
            }
            send_to_backend(cls.event_type, NETWORKS[block_event.network.type]['queue'], message)


class DucTransferMonitor(TransferMonitor):
    network_type = ['DUCATUS_MAINNET']
    currency = 'DUC'
