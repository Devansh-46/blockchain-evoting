from cryptography.fernet import Fernet
from django.conf import settings

def generate_key():
    return Fernet.generate_key()

def encrypt_vote(vote_data):
    key = settings.ENCRYPTION_KEY
    f = Fernet(key)
    encrypted_data = f.encrypt(vote_data.encode())
    return encrypted_data

def decrypt_vote(encrypted_data):
    key = settings.ENCRYPTION_KEY
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()