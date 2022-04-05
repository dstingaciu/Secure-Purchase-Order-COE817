from rsa import rsaKeyServer
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import time
import uuid
import multiprocessing as mp
import org_helpers
import socket

org_name = "Bueno, Damas & Stingaciu Fulfillment Co."

"""Helper Functions"""
delim = ";==;"

class key_server:
    def __init__(self, rsaObj):
        self.rsaOrg = rsaObj# Init RSA Class to generate key
        
    def initConnection(self, s):
        # Get socket
        self.s = s

        # Send public key from current private key instance
        pubKeyStr = self.rsaOrg.key.public_key().export_key().decode()
        firstResponse = f"{pubKeyStr}{delim}{org_name}".encode()
        self.s.send(firstResponse)

        # Await client public key
        pubClient_str, ts = self.s.recv(1024).decode().split(delim)

        # Verify time stamp is within 10 seconds
        self.__timestampGate(int(ts), self.s)

        # Import client public key
        self.pubClientStr = pubClient_str
        self.pubClient = PKCS1_v1_5.new(RSA.import_key(pubClient_str))

        # Begin key exchange verification process
        self.beginKeyExchangeVerification()


    def beginKeyExchangeVerification(self):
        # Receive N1 from client
        N1_enc = self.s.recv(1024)
        N1, ts = self.rsaOrg.decryptMessage(N1_enc).split(delim)
        ts = int(ts)

        self.__timestampGate(ts, self.s) # Verify time stamp is within 10 seconds

        # Generate N2
        N2 = uuid.uuid4().hex

        # Prepare N1, N2, TS string
        N1N2_str = f"{N1}{delim}{N2}{delim}{self.__returnCurrentTime()}"

        # Send encrypted N1, N2, TS string
        self.s.send(self.pubClient.encrypt(str.encode(N1N2_str)))

        N2_check_enc = self.s.recv(1024)
        N2_check, ts = self.rsaOrg.decryptMessage(N2_check_enc).split(delim)

        # N2 Checking
        if(N2_check != N2):
            self.s.send("N2 unverified, closing socket!")
            self.s.close()
            return False

        # Verifty time stamp is within 10 seconds
        self.__timestampGate(int(ts), self.s)

        # Go to email retreieval step
        self.retrieveEmail()

    def retrieveEmail(self):
        # Retrieve email address from user
        email_enc = self.s.recv(1024)
        email, ts = self.rsaOrg.decryptMessage(email_enc).split(delim)

        self.__timestampGate(int(ts), self.s)
        
        self.s.send(self.pubClient.encrypt(str.encode("added")))

        self.s.close()
        if(org_helpers.addToSessionKeys(email, self.pubClientStr)):
            return True
        else:
            return False

    def retrieveKey(self):
        return self.rsaOrg

    # Returns current time in milliseconds from epoch (INT)
    def __returnCurrentTime(self):
        return int(time.time_ns() / 1000)

    # Verifies incoming timestamps are within 60 seconds
    def __timestampGate(self,ts, s):
        if(self.__returnCurrentTime() - ts > 60000 or s is None):
                s.send(b"Timed out!")
                s.close()
                return False




