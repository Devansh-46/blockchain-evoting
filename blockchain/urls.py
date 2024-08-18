# blockchain/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    LoginView, 
    GetBlockchainView, 
    MineBlockView, 
    NewTransactionView, 
    RegisterVoterView, 
    RegisterCandidateView
)
from .views import ElectionViewSet, VoteHistoryViewSet

router = DefaultRouter()
router.register(r'elections', ElectionViewSet)
router.register(r'vote-history', VoteHistoryViewSet, basename='vote-history')

urlpatterns = [
    path('chain/', GetBlockchainView.as_view(), name='get_chain'),
    path('mine/', MineBlockView.as_view(), name='mine_block'),
    path('transactions/new/', NewTransactionView.as_view(), name='new_transaction'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('blockchain/', GetBlockchainView.as_view(), name='get_blockchain'),
    path('mine/', MineBlockView.as_view(), name='mine_block'),
    path('transaction/new/', NewTransactionView.as_view(), name='new_transaction'),
    path('register/voter/', RegisterVoterView.as_view(), name='register_voter'),
    path('register/candidate/', RegisterCandidateView.as_view(), name='register_candidate'),
    path('', include(router.urls)),
]

