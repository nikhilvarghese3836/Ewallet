from rest_framework import serializers
from .models import Transaction


def validate_reference_id(value):
    reference_id = ''.join(str(value).split('-'))
    if reference_id and Transaction.objects.filter(reference_id__exact=reference_id).exists():
        raise serializers.ValidationError("reference_id already exists!")
    return value


class TransactionSerializer(serializers.Serializer):
    reference_id = serializers.UUIDField(validators=[validate_reference_id])
    amount = serializers.FloatField()
