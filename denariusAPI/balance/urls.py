from django.conf.urls import url
from django.urls import path

from denariusAPI.balance.views import BalanceView

urlpatterns = [
    path(r'<str:address>/', BalanceView.as_view(), name='create-user'),
]
