from django.conf.urls import url

from denariusAPI.history.views import HistoryView             

urlpatterns = [
    url(r'^$', HistoryView.as_view(), name='get-transaction-history'),
]

