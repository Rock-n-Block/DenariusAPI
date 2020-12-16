from bip32utils import BIP32Key
from eth_keys import keys

from django.db import models
from django.contrib.auth.models import User

from denariusAPI.consts import MAX_DIGITS
from denariusAPI.settings import ROOT_KEYS, IS_TESTNET_PAYMENTS
from denariusAPI.exchange_requests.api import get_root_key
from denariusAPI.bip32_ducatus import DucatusWallet


class DucatusUser(models.Model):
    address = models.CharField(max_length=50, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_keys(self):
        duc_root_key = DucatusWallet.deserialize(ROOT_KEYS['ducatus']['public'])
        address = duc_root_key.get_child(self.id, is_prime=False).to_address()
        self.address = address
        self.save()
