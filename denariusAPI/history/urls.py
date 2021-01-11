from django.conf.urls import url
from django.urls import path

from denariusAPI.history.views import HistoryView, TransactionView

urlpatterns = [
    path('tx/<str:tx_hash>/', TransactionView.as_view(), name='get-transaction'),
    path('<str:address>/', HistoryView.as_view(), name='get-transaction-history'),
]

