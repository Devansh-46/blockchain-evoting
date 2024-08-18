from django.db import models
from django.contrib.auth.models import User
from .encryption import encrypt_vote, decrypt_vote
import secrets

def generate_voter_id():
    return secrets.token_hex(16)  # generates a 32-character hexadecimal string

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=32, unique=True, default=generate_voter_id)
    has_voted = models.BooleanField(default=False)
    voted_for = models.ForeignKey('Candidate', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Candidate(models.Model):
    name = models.CharField(max_length=255)
    party = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def get_vote_count(self):
        return Transaction.objects.filter(candidate=self).count()
    

class Transaction(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    encrypted_vote = models.BinaryField()

    def save(self, *args, **kwargs):
        vote_data = f"{self.voter.id}:{self.candidate.id}"
        self.encrypted_vote = encrypt_vote(vote_data)
        super().save(*args, **kwargs)

    def get_decrypted_vote(self):
        return decrypt_vote(self.encrypted_vote)
    
    def __str__(self):
        return f"{self.voter} voted for {self.candidate} at {self.timestamp}"
    
    
