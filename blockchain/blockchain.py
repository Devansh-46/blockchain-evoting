from .models import Block, Transaction
from django.utils import timezone
import hashlib
import json

class Blockchain:
    def create_genesis_block(self):
        genesis_block = Block.objects.create(
            index=0,
            previous_hash="0",
            data=json.dumps({"transactions": []}),
            nonce=0
        )
        genesis_block.hash = self.hash_block(genesis_block)
        genesis_block.save()
        return genesis_block

    def add_block(self, transactions):
        try:
            previous_block = self.get_latest_block()
        except Block.DoesNotExist:
            previous_block = self.create_genesis_block()

        new_block = Block.objects.create(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            timestamp=timezone.now(),
            data=json.dumps({"transactions": transactions}),
            nonce=0
        )
        new_block.hash = self.hash_block(new_block)
        new_block.save()
        return new_block

    def is_chain_valid(self):
        blocks = Block.objects.all().order_by('index')
        for i in range(1, len(blocks)):
            current_block = blocks[i]
            previous_block = blocks[i-1]
            if current_block.previous_hash != previous_block.hash:
                return False
            if self.hash_block(current_block) != current_block.hash:
                return False
        return True

    def get_latest_block(self):
        return Block.objects.latest('index')

    @staticmethod
    def hash_block(block):
        block_string = f"{block.index}{block.timestamp}{block.previous_hash}{block.nonce}{block.data}".encode()
        return hashlib.sha256(block_string).hexdigest()