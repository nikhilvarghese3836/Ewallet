import datetime
from uuid import UUID
from xmlrpc.client import boolean
from django.http import JsonResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Wallet
from .serializers import WalletSerializer


class WalletInitialization(APIView):
    permission_classes = [AllowAny]

    def post(self, request,):
        try:
            '''Initialize account for wallet'''
            wallet_serializer = WalletSerializer(data=request.data)
            if not wallet_serializer.is_valid():
                return JsonResponse({"status": "fail", "data": {"error": wallet_serializer.errors}}, status=HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                wallet_ins = Wallet(
                    owned_by=request.data.get('customer_xid'),
                )
                wallet_ins.save()
            token, _ = Token.objects.get_or_create(user=wallet_ins)

            return JsonResponse({"status": "success", "data": {"token": token.key}},
                                status=HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Something went wrong.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class WalletManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        '''View wallet balance'''
        try:
            wallet_ins = request.user
            if wallet_ins.status == 'enabled':
                return JsonResponse({"status": "success", "data": {"wallet": wallet_ins.serialize()}},
                                    status=HTTP_200_OK)

            return JsonResponse({"status": "fail", "data": {"error": "Disabled"}},
                                status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Something went wrong.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    permission_classes = [IsAuthenticated]

    def post(self, request,):
        '''Enable wallet'''
        try:
            wallet_ins = request.user
            if wallet_ins.status == 'enabled':
                return JsonResponse({"status": "fail", "data": {"error": "Already enabled."}},
                                    status=HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                wallet_ins.status = "enabled"
                wallet_ins.enabled_at = datetime.datetime.now()
                wallet_ins.save()
            return JsonResponse({"status": "success", "data": {"wallet": wallet_ins.serialize()}},
                                status=HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Something went wrong.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    permission_classes = [IsAuthenticated]

    def patch(self, request,):
        '''Disable wallet'''
        try:
            wallet_ins = request.user
            is_disabled = request.data.get('is_disabled')
            if not is_disabled:
                return JsonResponse({"status": "fail", "data": {"error": {"is_disabled": ["no data for field."]}}}, status=HTTP_400_BAD_REQUEST)
            if is_disabled != 'true':
                return JsonResponse({"status": "fail", "data": {"error": {"is_disabled": ["not valid data for field."]}}}, status=HTTP_400_BAD_REQUEST)
            if wallet_ins.status == 'disabled':
                return JsonResponse({"status": "fail", "data": {"error": "Already disabled."}},
                                    status=HTTP_400_BAD_REQUEST)
            if is_disabled:
                with transaction.atomic():
                    wallet_ins.status = "disabled"
                    wallet_ins.disabled_at = datetime.datetime.now()
                    wallet_ins.save()
                return JsonResponse({"status": "success", "data": {"wallet": wallet_ins.serialize()}},
                                    status=HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': 'Something went wrong.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
