from pubsub import pub

from eventscanner.monitors.payments import DucPaymentMonitor
from eventscanner.monitors import transfer

pub.subscribe(DucPaymentMonitor.on_new_block_event, 'DUCATUS_MAINNET')
pub.subscribe(transfer.DucTransferMonitor.on_new_block_event, 'DUCATUS_MAINNET')
