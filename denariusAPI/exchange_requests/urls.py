from django.conf.urls import url

from denariusAPI.exchange_requests.views import ExchangeRequestView

urlpatterns = [
    url(r'^$', ExchangeRequestView.as_view(), name='create-exchange-request'),
]