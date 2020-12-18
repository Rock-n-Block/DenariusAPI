from eventscanner.queue.pika_handler import send_to_backend
from mywish_models.models import ExchangeRequests, session
from scanner.events.block_event import BlockEvent
from settings.settings_local import NETWORKS


class EthPaymentMonitor:

    network_types = ['ETHEREUM_MAINNET']
    event_type = 'payment'
    queue = NETWORKS[network_types[0]]['queue']
    count=0
    currency = 'ETH'

    @classmethod
    def address_from(cls, model):
        s = 'generated_address'
        return getattr(model, s)

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if cls.count==0:
            print('here')
            cls.count+=1
            message={'userID': 404, 'amount': 20000000000000000, 'address': '0xa9551C555e31847A596059b02dcf6FB05a80eC5a', 'status': 'COMMITTED'}
            send_to_backend('withdraw', cls.queue, message)

        print('alive', flush=True)
        if block_event.network.type not in cls.network_types:
            return

        addresses = block_event.transactions_by_address.keys()
        query_result = session.query(ExchangeRequests).filter(cls.address_from(ExchangeRequests).in_(addresses)).all()
        for model in query_result:
            address = cls.address_from(model)
            print('address: {}'.format(address), flush=True)
            transactions = block_event.transactions_by_address[address.lower()]

            if not transactions:
                print('{}: User {} received from DB, but was not found in transaction list (block {}).'.format(
                    block_event.network.type, model, block_event.block.number))

            for transaction in transactions:
                if address.lower() != transaction.outputs[0].address.lower():
                    print('{}: Found transaction out from internal address. Skip it.'.format(block_event.network.type),
                          flush=True)
                    continue

                tx_receipt = block_event.network.get_tx_receipt(transaction.tx_hash)

                message = {
                    'userID': model.userID,
                    'address': address,
                    'transactionHash': transaction.tx_hash,
                    'currency': cls.currency,
                    'amount': transaction.outputs[0].value,
                    'success': tx_receipt.success,
                    'status': 'COMMITTED'
                }

                send_to_backend(cls.event_type, cls.queue, message)


class DucxPaymentMonitor(EthPaymentMonitor):
    network_types = ['DUCATUSX_MAINNET']
    queue = NETWORKS[network_types[0]]['queue']

    currency = 'DUCX'
