from django.conf.urls import url

from denariusAPI.transfers.views import TransferView, HistoryView

urlpatterns = [
    url('transfer/'r'^$', TransferView.as_view(), name='create-transfer'),
    url(r'^$', HistoryView.as_view(), name='get-transaction-history'),
]