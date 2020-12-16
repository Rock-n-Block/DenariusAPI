from django.conf.urls import url

from denariusAPI.balance.views import BalanceView

urlpatterns = [
    url(r'^$', BalanceView.as_view(), name='create-exchange-request'),
]