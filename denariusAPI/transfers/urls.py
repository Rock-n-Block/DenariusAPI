from django.conf.urls import url

from denariusAPI.transfers.views import TransferView

urlpatterns = [
    url(r'^$', TransferView.as_view(), name='create-transfer'),
]
