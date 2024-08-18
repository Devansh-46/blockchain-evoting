from django.test import TestCase, TransactionTestCase
from django.db import connection
from django.core.management import call_command
from .blockchain import Blockchain
from .models import Block, Voter, Candidate, Election
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib
import json

class BlockchainTestCase(TransactionTestCase):
    def setUp(self):
        call_command('migrate')
        self.blockchain = Blockchain()
        self.user1 = User.objects.create_user(username='voter1', password='password1')
        self.user2 = User.objects.create_user(username='voter2', password='password2')
        self.voter1 = Voter.objects.create(user=self.user1)
        self.voter2 = Voter.objects.create(user=self.user2)
        self.election = Election.objects.create(
            name='Test Election',
            description='Test Description',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1)
        )
        self.candidate1 = Candidate.objects.create(name='Candidate 1', election=self.election)
        self.candidate2 = Candidate.objects.create(name='Candidate 2', election=self.election)

    def tearDown(self):
        call_command('flush', verbosity=0, interactive=False)

    def test_block_creation(self):
        block = self.blockchain.create_genesis_block()
        self.assertIsInstance(block, Block)
        self.assertEqual(block.index, 0)
        self.assertEqual(block.data, json.dumps({"transactions": []}))
        self.assertEqual(block.previous_hash, '0')

    def test_block_hash(self):
        block = self.blockchain.create_genesis_block()
        expected_hash = self.blockchain.hash_block(block)
        self.assertEqual(block.hash, expected_hash)

    def test_add_block(self):
        initial_length = Block.objects.count()
        self.blockchain.add_block([])
        self.assertEqual(Block.objects.count(), initial_length + 2)  # Genesis block + new block
        latest_block = self.blockchain.get_latest_block()
        self.assertEqual(latest_block.data, json.dumps({"transactions": []}))
        self.assertEqual(latest_block.index, 1)

    def test_chain_validity(self):
        self.blockchain.create_genesis_block()
        self.blockchain.add_block([])
        self.blockchain.add_block([])
        self.assertTrue(self.blockchain.is_chain_valid())

        # Tamper with the chain
        block = Block.objects.get(index=1)
        block.data = json.dumps({"transactions": ["tampered_data"]})
        block.save()
        self.assertFalse(self.blockchain.is_chain_valid())