from uuid import UUID
from rest_framework import serializers
from .models import Wallet


def validate_customer_xid(value):
    customer_xid = ''.join(str(value).split('-'))
    if customer_xid and Wallet.objects.filter(owned_by__exact=customer_xid).exists():
        raise serializers.ValidationError("customer_xid already exists!")
    return value


class WalletSerializer(serializers.Serializer):
    customer_xid = serializers.UUIDField(validators=[validate_customer_xid])
