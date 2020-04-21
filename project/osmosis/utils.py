from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
from Crypto.Cipher import AES
import base64

#this is your "password/ENCRYPT_KEY". keep it in settings.py file
#key = Fernet.generate_key() 

import logging, uuid
logger = logging.getLogger(__name__)

def encrypt_val(clear_text):
    enc_secret = AES.new(settings.ENCRYPT_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    return cipher_text


def decrypt_val(cipher_text):
    dec_secret = AES.new(settings.ENCRYPT_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val