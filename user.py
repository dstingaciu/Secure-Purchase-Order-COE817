import random
import uuid
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from rsa import rsaKeyServer
import socket
import time
import json
from send_email import send_email

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

# Inititate Private and public RSA key
user_public_key = rsaKeyServer()

my_email = "coe817finalproject@gmail.com"

delim = ";==;"
class key_exchange_with_org_key_server:
    def __init__(self):
        self.s = socket.socket()
        self.ksPort = 60000
        self.orgServer = "127.0.0.1"

    def initConnection(self):
        # Initiate connection to org key server
        self.s.connect((self.orgServer, self.ksPort))

        # Receive public key string and org name
        orgPubStr, orgName = self.s.recv(1024).decode().split(delim)
        print("Welcome to " + orgName)

        # Convert public key string to usable public key
        self.orgPub = PKCS1_v1_5.new(RSA.import_key(orgPubStr))

        # Prepare client key string and TS response
        clientPubKeyStr = user_public_key.key.public_key().export_key().decode()
        firstClientResponse = f"{clientPubKeyStr}{delim}{returnCurrentTime()}".encode()

        # Send client key
        self.s.send(firstClientResponse)
        
        self.beginKeyExchangeVerification()

    def beginKeyExchangeVerification(self):
        # Generate random N1
        N1 = uuid.uuid4().hex

        # Prepare N1 Str and encrypt with org public key
        N1Str = f"{N1}{delim}{returnCurrentTime()}"
        N1_enc = self.orgPub.encrypt(str.encode(N1Str))

        # Send encrypted N1 Str
        self.s.send(N1_enc)

        # Receive N1, N2, TS Str and split message
        N1N2_enc = self.s.recv(2048)
        N1_check, N2, TS = user_public_key.decryptMessage(N1N2_enc).split(delim)

        # Check N1
        if(N1_check != N1):
            self.s.send("N1 unverified, closing socket!")
            self.s.close()
            return

        # Verify time stamp is within 10 seconds
        timestampGate(int(TS), self.s)

        # Prepare N2 string
        N2Str = f"{N2}{delim}{returnCurrentTime()}"

        # Send N2 String
        self.s.send(self.orgPub.encrypt(str.encode(N2Str)))
        
        self.sendUserEmailToKs()

    def sendUserEmailToKs(self):
        # Setup email string
        email_str = f"{my_email}{delim}{returnCurrentTime()}"
        self.s.send(self.orgPub.encrypt(str.encode(email_str)))

        ack_enc = self.s.recv(1024)
        print(ack_enc)
        ack_str = user_public_key.decryptMessage(ack_enc)
        
        if(ack_str.strip() == "added"):
            print("Added session key!")

        self.s.close()

    def getOrgPublicKey(self):
        return self.orgPub

"""
Class for asking user what they wish to order and then signing and hashing order
"""
class itemUICLI:
    def __init__(self, kskey):
        self.purchaseOrder = []
        self.kskey = kskey

    # UI for the user to see what items they wish to order
    def uiFlow(self):
        doneOrdering = 0
        
        while(doneOrdering == 0):
            # Prompt user for an item number from catalog
            print("Enter an item number (enter -1 to finish adding items): ")
            itemNum = input()

            # Check if we should be done ordering
            if(itemNum == "-1"):
                doneOrdering = 1
            else:
                # Prompt user for quantity of item to purchase
                print("How much of "+ itemNum + " would you like to purchase? (enter -1 to cancel this item): ")
                quantity = input()
                self.purchaseOrder.append({"ItemNum": itemNum, "quantity": quantity})
                print("Added "+quantity+ " of " + itemNum)
            
            print("\n")

        self.hashPurchaseObject()

    def hashPurchaseObject(self):
        # Generate JSON string from array of purchases
        orderString = json.dumps(self.purchaseOrder)
        
        # Get time stamp
        timestamp = returnCurrentTime()

        # Combine JSON string and timestamp
        dec_orderString = f"{orderString}{delim}{timestamp}"

        # Generate signed order hash from JSON String + timestamp
        signedOrderHash, signedOrderDigest = user_public_key.signMessage(str.encode(dec_orderString))

        # Encrypt JSON string + timestamp
        enc_orderString = self.kskey.encrypt(str.encode(dec_orderString))

        send_email(f"{signedOrderHash}{delim}{enc_orderString}")

    def returnPO(self):
        return self.purchaseOrder


ks_ex = key_exchange_with_org_key_server()
ks_ex.initConnection()

cli = itemUICLI(ks_ex.getOrgPublicKey())
cli.uiFlow()