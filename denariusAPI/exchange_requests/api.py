import binascii
import requests

from denariusAPI.settings import ROOT_KEYS, IS_TESTNET_PAYMENTS



def generate_memo(m):
    memo_str = os.urandom(8)
    m.update(memo_str)
    memo_str = binascii.hexlify(memo_str + m.digest()[0:2])
    return memo_str


def get_root_key():
    network = 'mainnet'

    if IS_TESTNET_PAYMENTS:
        network = 'testnet'

    root_pub_key = ROOT_KEYS[network]['public']

    return root_pub_key
