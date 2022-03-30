from rsa import rsaKeyServer
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import socket
import time
import uuid
import multiprocessing as mp
import org_helpers

org_name = "Bueno, Damas & Stingaciu Fulfillment Co."

"""Helper Functions"""

# Returns current time in milliseconds from epoch (INT)
def returnCurrentTime():
    return int(time.time_ns() / 1000)

# Verifies incoming timestamps are within 10 seconds
def timestampGate(ts, s):
    if(returnCurrentTime() - ts > 10000 or s is None):
            s.send("Timed out!")
            s.close()
            exit(-1)

delim = ";==;"

class key_server:
    def __init__(self, s):
        self.rsaOrg = rsaKeyServer() # Init RSA Class to generate key
        self.s = s
        

    def initConnection(self):
        # Send public key from current private key instance
        pubKeyStr = self.rsaOrg.key.public_key().export_key().decode()
        firstResponse = f"{pubKeyStr}{delim}{org_name}".encode()
        self.s.send(firstResponse)

        # Await client public key
        pubClient_str, ts = self.s.recv(1024).decode().split(delim)

        # Verify time stamp is within 10 seconds
        timestampGate(int(ts), self.s)

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

        timestampGate(ts, self.s) # Verify time stamp is within 10 seconds

        # Generate N2
        N2 = uuid.uuid4().hex

        # Prepare N1, N2, TS string
        N1N2_str = f"{N1}{delim}{N2}{delim}{returnCurrentTime()}"

        # Send encrypted N1, N2, TS string
        self.s.send(self.pubClient.encrypt(str.encode(N1N2_str)))

        N2_check_enc = self.s.recv(1024)
        N2_check, ts = self.rsaOrg.decryptMessage(N2_check_enc).split(delim)

        # N2 Checking
        if(N2_check != N2):
            self.s.send("N2 unverified, closing socket!")
            self.s.close()
            exit(-1)

        # Verifty time stamp is within 10 seconds
        timestampGate(int(ts), self.s)

        # Go to email retreieval step
        self.retrieveEmail()

    def retrieveEmail(self):
        # Retrieve email address from user
        email_enc = self.s.recv(1024)
        email, ts = self.rsaOrg.decryptMessage(email_enc).split(delim)

        timestampGate(int(ts), self.s)
        
        self.s.send(self.pubClient.encrypt(str.encode("added")))

        self.s.close()
        if(org_helpers.addToSessionKeys(email, self.pubClientStr)):
            exit(1)
        else:
            exit(-1)

def beginKeyServerSession(s):
    ks = key_server(s)
    ks.initConnection()

# Setup connection socket
s = socket.socket()
port = 60000
host = socket.gethostname()
s.bind(('127.0.0.1', port))     # Bind to the port
s.listen(5)                     # Now wait for client connection

print("await connection from client...")
# Await connection from a client
conn, addr = s.accept()

beginKeyServerSession(conn)



