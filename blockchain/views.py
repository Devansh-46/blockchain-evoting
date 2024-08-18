# blockchain/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Election, Candidate, Vote
from .serializers import ElectionSerializer, CandidateSerializer, VoteSerializer

class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def cast_vote(self, request, pk=None):
        election = self.get_object()
        candidate_id = request.data.get('candidate_id')
        
        if not candidate_id:
            return Response({'error': 'Candidate ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = Candidate.objects.get(id=candidate_id, election=election)
        except Candidate.DoesNotExist:
            return Response({'error': 'Invalid candidate'}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote.objects.create(user=request.user, election=election, candidate=candidate)
        return Response({'message': 'Vote cast successfully'}, status=status.HTTP_201_CREATED)

class VoteHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user).order_by('-timestamp')
    
class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'candidate_id'
    http_method_names = ['get']
    filterset_fields = ['election']
    search_fields = ['name', 'election__name']
    ordering_fields = ['name', 'election__name']
    ordering = ['name']
    extra_kwargs = {
        'url': {'lookup_field': 'id'}
    }

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Election, Candidate, Vote

class RegisterView(APIView):
    def post(self, request):
        # Implementation for user registration
        pass


class LoginView(APIView):
    def post(self, request):
        # Implementation for user login
        pass

class GetBlockchainView(APIView):
    def get(self, request):
        # Implementation to get blockchain data
        pass

class MineBlockView(APIView):
    def post(self, request):
        # Implementation to mine a new block
        pass

class NewTransactionView(APIView):
    def post(self, request):
        # Implementation to create a new transaction
        pass

class RegisterVoterView(APIView):
    def post(self, request):
        # Implementation to register a voter
        pass

class RegisterCandidateView(APIView):
    def post(self, request):
        # Implementation to register a candidate
        pass

# Add any other views you might have...