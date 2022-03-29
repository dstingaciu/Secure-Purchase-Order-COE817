from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class rsaEx():
    """ 
    Init function
            initializes rsa key using RSA.generate and PKCS1 RSA encryption
    """
    def __init__(self):
        self.key = RSA.generate(2048) # Generate RSA Key
        self.cipher = PKCS1_v1_5.new(self.key) # Create cipher text using PKCS1_V1_5 and RSA key
        self.privateCipher = pkcs1_15.new(self.key) # Create private cipher text for signing
        self.sentinel = 0 # Default sentinel for decryption
    """ 
    Encrypt Message
            Encrypts a given message

            param message: Message to encrypt
    """
    def encryptMessage(self, message):
        self.sentinel = len(message) # Set sentinel to message length
        return self.cipher.encrypt(str.encode(message)) # Encrypt message using PKCS1 RSA Encryption
    """
    Sign Message
        return the signature of a message using the private key
    """
    def signMessage(self, message):
        messageHash = SHA256.new(message)
        return self.privateCipher.sign(messageHash), messageHash
    """
    Decrypt Message
            Decrypts a given encrypted phrase

            param encrypted: Encrypted message to decrypt
    """
    def decryptMessage(self, encrypted):
        return self.cipher.decrypt(encrypted, -1).decode()  # Decrypt message using PKCS1 RSA Decrpytion