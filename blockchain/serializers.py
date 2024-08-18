# blockchain/serializers.py

from rest_framework import serializers
from .models import Election, Candidate, Vote

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'party']

class ElectionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'candidates']

class VoteSerializer(serializers.ModelSerializer):
    election = serializers.StringRelatedField()
    candidate = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ['id', 'election', 'candidate', 'timestamp']