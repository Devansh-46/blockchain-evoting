from rest_framework import viewsets, response, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Voter, Transaction
from serializers import TransactionSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_voter(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        voter = Voter.objects.create(user=user)
        return response.Response({
            'message': 'Voter registered successfully',
            'voter_id': voter.voter_id
        }, status=status.HTTP_201_CREATED)
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request):
        transactions = self.get_queryset()
        decrypted_transactions = [
            {
                'id': t.id,
                'voter': t.voter.voter_id,
                'candidate': t.candidate.id,
                'timestamp': t.timestamp,
                'decrypted_vote': t.get_decrypted_vote()
            }
            for t in transactions
        ]
        return response.Response(decrypted_transactions)

    def perform_create(self, serializer):
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return Transaction.objects.all().select_related('voter', 'candidate')

    def list(self, request):
        transactions = self.get_queryset()
        decrypted_transactions = [
            {
                'id': t.id,
                'voter': t.voter.id,
                'candidate': t.candidate.id,
                'timestamp': t.timestamp,
                'decrypted_vote': t.get_decrypted_vote()
            }
            for t in transactions
        ]
        return response.Response(decrypted_transactions)
    
    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

