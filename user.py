import uuid
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_v1_5, DES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from datetime import datetime
from rsa import rsaEx
import socket
"""
Global Variables

Variables for standard deliminator

DELIM           : Delimiator between message/data and packet #
time_format     : standard time format
s               : socket variable used for communication with responder/server

session_key_str : binary string containing session key using DES sencryption to encrypt/decrypt session data

s_key           : DES class key initialized using session_key_str

IDa             : ID of initiator/client
"""

DELIM = ";==;"
time_format = "%m/%d/%Y;%H:%M:%S"

rsa = rsaEx() # Initiate our RSA key and cipher
pubA_key = rsa.key.public_key().export_key() # PubB

session_key_str = b"RYERSON "

s_key = DES.new(session_key_str, DES.MODE_ECB) # init session key

s = socket.socket()             # Create a socket object
port = 60000                    # Reserve a port for your service.

IDa = b"INITIATOR A"

def encrypt(Plaintext_pad, key):
    if(isinstance(Plaintext_pad, str)):
        byteEncodedMessage = str.encode(Plaintext_pad) # Encode message in base 64
    else:
        byteEncodedMessage = Plaintext_pad
    return key.encrypt(pad(byteEncodedMessage, 8)) # Encrypt message using given key

def decrypt(ciphertext, key):
    return key.decrypt(ciphertext)

# Initiates connection to server on a given port and handshake for session key
def initConnection():
    print("Initiating connection to server...")

    # INITIATE CONNECTION TO SERVER
    s.connect(('127.0.0.1', port))
    print("Connection initiated!")
    # == EXCHANGE KEYS == #

    # SEND PUB A KEY TO SERVER
    print("Sending PUB A: ", pubA_key)
    s.send(pubA_key)

    # AWAIT ENCRYPTED PUB B KEY
    pubB_key = s.recv(1024)
    print("Received PUB B: ", pubB_key)
    # ==================== #

    # == GENERATE N1 STRING AND SEND IT TO SERVER ENCRYPTED USING PUB B == #
    N1 = uuid.uuid4().hex # Generate Nonce 1
    print("N1 generated: ", N1)
    rsaB = RSA.import_key(pubB_key) # import key
    keyExCipher = PKCS1_v1_5.new(rsaB) # create cipher

    nonceIdStr = f"{N1}||{IDa}" # Create N1 Str
    print("Sending N1 with ID: ",nonceIdStr)
    encryptedInitStr = keyExCipher.encrypt(str.encode(nonceIdStr)) # Encrypt N1 Str with Pub B key

    s.send(encryptedInitStr) # Send

    # =================================================================== #

    # Recieve and Decrypt N1 || N2 Str
    encNonceOneTwoStr = s.recv(1024)
    decNonceOneTwoStr = rsa.decryptMessage(encNonceOneTwoStr).split("||")
    print("Received N1||N2 String (Encrypted): ", encNonceOneTwoStr)
    print("Received N1||N2 String (Decrypted): ",decNonceOneTwoStr)

    # Extract N1 and N2
    recN1 = decNonceOneTwoStr[0]
    N2 = decNonceOneTwoStr[1]

    # If mismatch, end connection and exit program
    print("Verifying N1...")
    if(recN1 != N1):
        print("Error establishing secure connection to server, N1 != N2")
        s.close()
        exit(-1)
    print("Verified!")
    # Encrypt received N2 and send for verification
    verifyN2 = keyExCipher.encrypt(str.encode(N2))
    print("Sending back N2 for verification: ", N2)
    s.send(verifyN2)

    encACK = s.recv(1024)
    decACK = rsa.decryptMessage(encACK).split("||")
    print("Received N2 ACK (Encrypted): ",encACK)
    print("Received N2 ACK (Decrypted): ",decACK)

    if(decACK[0] != "ACK" or decACK[1] != N2):
        print("Error establishing secure connection to server, N2 mismatch on ACK")
        s.close()
        exit(-1)
    
    print("Beginning session key sending process")
    #encSKeyStr = rsa.encryptMessage(session_key_str.decode()) # Encrypt Session key using PR Ap
    signedSKey, digest = rsa.signMessage(session_key_str)
    encSessionKey = keyExCipher.encrypt(session_key_str)
    print("Sending signature of session key string using Pub A and session key string: ")
    print("Signed session key string: ",signedSKey)
    print("Session Key string: ", session_key_str)
    packet = signedSKey + "||".encode() + encSessionKey

    s.send(packet)

    sKeyACK = s.recv(1024)
    decSKeyAck = decrypt(sKeyACK, s_key).decode()
    print("GOT ACK ", decSKeyAck)
    return True