from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Transaction
from .serializers import TransactionSerializer

@api_view(['GET'])
def transaction_history(request):
    \"\"\"Get user transaction history\"\"\"
    try:
        wallet = request.user.wallet
    except:
        return Response({
            'error': 'Wallet not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    transactions = Transaction.objects.filter(wallet=wallet)
    
    # Pagination
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    paginator = Paginator(transactions, page_size)
    page_obj = paginator.get_page(page)
    
    serializer = TransactionSerializer(page_obj, many=True)
    
    return Response({
        'transactions': serializer.data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_transactions': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    }, status=status.HTTP_200_OK)