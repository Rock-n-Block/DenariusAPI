from django.conf.urls import url
from django.urls import path

from denariusAPI.history.views import HistoryView             

urlpatterns = [
    path('<str:address>/', HistoryView.as_view(), name='get-transaction-history'),
]

