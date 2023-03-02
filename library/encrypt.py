import random
import string
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64
from datetime import timezone
import datetime 
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
def random_string(letter_count, digit_count):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    return final_string


def encrypt(t):
    chars = list(t)
    allowed_characters = list(" dfikmnVopq7rsjtGuvwMxhHyazA-eBCEcFDIJQ*KlN5OPb:2RSgTUWXYZ013468L9,.?!@$%&")
    temp = ''
    for char in chars:
        for i in allowed_characters:
            if char == i:
                chars[chars.index(char)] = allowed_characters.index(i)
                temp = temp + str(allowed_characters.index(i))
    return temp
def encrypt_message(message, key):
    print(key)
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_message = message + (DES3.block_size - len(message) % DES3.block_size) * chr(DES3.block_size - len(message) % DES3.block_size)
    encrypted_message = cipher.encrypt(padded_message.encode())
    return base64.b64encode(encrypted_message).decode()
def encrypt(to_encrypt, key):
    key_bytes = bytes(key, 'utf-8')
    key_hash = hashes.Hash(hashes.MD5(), backend=default_backend())
    key_hash.update(key_bytes)
    key_hash_bytes = key_hash.finalize()
    cipher = Cipher(algorithms.TripleDES(key_hash_bytes), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = PKCS7(algorithms.TripleDES.block_size).padder()
    padded_data = padder.update(to_encrypt.encode('utf-8')) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt(to_decrypt, key):
    key_bytes = bytes(key, 'utf-8')
    key_hash = hashes.Hash(hashes.MD5(), backend=default_backend())
    key_hash.update(key_bytes)
    key_hash_bytes = key_hash.finalize()
    cipher = Cipher(algorithms.TripleDES(key_hash_bytes), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = PKCS7(algorithms.TripleDES.block_size).unpadder()
    decrypted_data = decryptor.update(base64.b64decode(to_decrypt)) + decryptor.finalize()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode('utf-8')