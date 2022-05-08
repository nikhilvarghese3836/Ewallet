from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'wallet/deposits', views.TransactionDeposit.as_view(), name='deposit'),
    url(r'wallet/withdrawals', views.TransactionWithdrawal.as_view(), name='withdrawal'),
]