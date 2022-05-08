from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'init', views.WalletInitialization.as_view(), name='initializaion'),
    url(r'wallet', views.WalletManagement.as_view(), name='management'),
]