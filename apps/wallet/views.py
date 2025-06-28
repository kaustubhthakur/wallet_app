from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Wallet
from .serializers import WalletSerializer, WalletBalanceUpdateSerializer, WalletEnableSerializer
from apps.transactions.models import Transaction

@api_view(['POST'])
def enable_wallet(request):
    \"\"\"Enable/Disable user wallet\"\"\"
    try:
        wallet = request.user.wallet
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)
    
    serializer = WalletEnableSerializer(data=request.data)
    if serializer.is_valid():
        wallet.is_active = serializer.validated_data['is_active']
        wallet.save()
        
        return Response({
            'message': f'Wallet {"enabled" if wallet.is_active else "disabled"} successfully',
            'wallet': WalletSerializer(wallet).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_balance(request):
    \"\"\"Get user wallet balance\"\"\"
    try:
        wallet = request.user.wallet
        return Response({
            'balance': wallet.balance,
            'is_active': wallet.is_active,
            'wallet_id': wallet.id
        }, status=status.HTTP_200_OK)
    except Wallet.DoesNotExist:
        return Response({
            'error': 'Wallet not found. Please enable your wallet first.'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_balance(request):
    \"\"\"Update user wallet balance\"\"\"
    try:
        wallet = request.user.wallet
        if not wallet.is_active:
            return Response({
                'error': 'Wallet is not active'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Wallet.DoesNotExist:
        return Response({
            'error': 'Wallet not found. Please enable your wallet first.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WalletBalanceUpdateSerializer(
        data=request.data, 
        context={'wallet': wallet}
    )
    
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        transaction_type = serializer.validated_data['transaction_type']
        description = serializer.validated_data.get('description', '')
        
        with transaction.atomic():
            # Update wallet balance
            if transaction_type == 'credit':
                wallet.credit(amount)
            else:
                wallet.debit(amount)
            
            # Create transaction record
            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type=transaction_type,
                description=description
            )
        
        return Response({
            'message': f'Wallet {transaction_type}ed successfully',
            'new_balance': wallet.balance,
            'transaction': {
                'amount': amount,
                'type': transaction_type,
                'description': description
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)