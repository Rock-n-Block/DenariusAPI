from django.db import models

from denariusAPI.consts import MAX_DIGITS
from denariusAPI.exchange_requests.models import DucatusUser


class DucatusTransfer(models.Model):
    ducatus_user = models.ForeignKey(DucatusUser, on_delete=models.CASCADE, null=True)
    tx_hash = models.CharField(max_length=100, null=True, default='')
    from_address = models.CharField(max_length=100, null=True, default='')
    to_address = models.CharField(max_length=100, null=True, default='')
    amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0)
    currency = models.CharField(max_length=50, null=True, default='DUC')
    transaction_fee = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0, default= 100000)
    number_of_confirmations = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0, default = 0)
    state = models.CharField(max_length=50, null=True, default='')
    created_date = models.DateTimeField(auto_now_add=True)
