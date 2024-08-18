from django.db import models
from django.contrib.auth import get_user_model
from django.apps import AppConfig
from django.utils import timezone
import hashlib

User = get_user_model()

class BlockchainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blockchain'

class Election(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

def default_hash():
    return hashlib.sha256(b"genesis_block").hexdigest()

class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_hash = models.CharField(max_length=64)
    nonce = models.IntegerField(default=0)
    hash = models.CharField(max_length=64, default=default_hash)
    data = models.TextField(default='')

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)