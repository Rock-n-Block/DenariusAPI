from pubsub import pub

from eventscanner.monitors.payments import DucxPaymentMonitor
from eventscanner.monitors import transfer

pub.subscribe(DucxPaymentMonitor.on_new_block_event, 'DUCATUSX_MAINNET')
pub.subscribe(transfer.DucxTransferMonitor.on_new_block_event, 'DUCATUSX_MAINNET')
