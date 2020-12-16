from rest_framework import serializers

from denariusAPI.transfers.models import DucatusTransfer

from denariusAPI.exchange_requests.models import DucatusUser


class DucatusTransferSerializer(serializers.ModelSerializer):
    ducatus_user = serializers.PrimaryKeyRelatedField(queryset=DucatusUser.objects)

    class Meta:
        model = DucatusTransfer
        fields = ('ducatus_user', 'tx_hash', 'amount', 'currency', 'state')
