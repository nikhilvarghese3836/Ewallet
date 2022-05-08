from django.http import JsonResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionDeposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        '''Add virtual money to wallet'''
        try:
            wallet_ins = request.user
            transaction_serializer = TransactionSerializer(data=request.data)
            if not transaction_serializer.is_valid():
                return JsonResponse({"status": "fail", "data": {"error": transaction_serializer.errors}}, status=HTTP_400_BAD_REQUEST)
            amount = float(request.data.get('amount'))
            reference_id = request.data.get('reference_id')
            with transaction.atomic():
                transaction_ins = Transaction(
                    transaction_by=wallet_ins,
                    transaction_type='deposit',
                    amount=amount,
                    reference_id=reference_id
                )
                transaction_ins.save()
                wallet_ins.balance += amount
                wallet_ins.save()
            return JsonResponse({"status": "success", "data": {"deposit": transaction_ins.serialize()}},
                                status=HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Something went wrong.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        '''Use virtual money from wallet'''
        try:
            wallet_ins = request.user
            transaction_serializer = TransactionSerializer(data=request.data)
            if not transaction_serializer.is_valid():
                return JsonResponse({"status": "fail", "data": {"error": transaction_serializer.errors}}, status=HTTP_400_BAD_REQUEST)
            amount = float(request.data.get('amount'))
            reference_id = request.data.get('reference_id')
            if wallet_ins.balance < amount:
                return JsonResponse({"status": "fail", "data": {"error": {"balance": ["Insufficient balance."]}}}, status=HTTP_422_UNPROCESSABLE_ENTITY)
            with transaction.atomic():
                transaction_ins = Transaction(
                    transaction_by=wallet_ins,
                    transaction_type='withdrawal',
                    amount=amount,
                    reference_id=reference_id
                )
                transaction_ins.save()
                wallet_ins.balance -= amount
                wallet_ins.save()
            return JsonResponse({"status": "success", "data": {"withdrawal": transaction_ins.serialize()}},
                                status=HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Something went wrong.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
