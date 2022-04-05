import json
from email_access import accessEmail
from org_helpers import retrieveStoredSessionKey, addToPurchaseOrderFromClient
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import ast

delim = ";==;"

class retrieveLatestPurchaseOrderRequests:
    def __init__(self, priv_key):
        self.priv = priv_key

    def retrieveEncryptedPO(self):
        fromEmail, encEmail = accessEmail()

        keyArr = retrieveStoredSessionKey(fromEmail)
        key_str = keyArr[0][0]

        signedOrderHash, enc_orderString = encEmail.split(delim)

        enc_orderString = ast.literal_eval(enc_orderString)
        signedOrderHashLiteral = ast.literal_eval(signedOrderHash)

        dec_PO_str = self.priv.decryptMessage(enc_orderString)


        obj, ts = dec_PO_str.split(delim)

        hashedPO = SHA256.new(str.encode(dec_PO_str))
        try:
            userRSA = RSA.import_key(key_str)
            pkcs1_15.new(userRSA).verify(hashedPO, signedOrderHashLiteral)
            addToPurchaseOrderFromClient(fromEmail, obj, signedOrderHash)
        except ValueError:
            print("Error! Failed to verify signature")
            addToPurchaseOrderFromClient(fromEmail, obj, signedOrderHash, 1)
        