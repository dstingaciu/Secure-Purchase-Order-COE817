# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 23:27:46 2022

@author: Riel Bueno
"""

#from ecdsa import SigningKey

#def depart(SupervisorPublicKey, UserPublicKey, hpoUser, hpoSupervisor, hpo):
    #private_key = SigningKey.generate() # uses NIST192p
    
    #supPublicKey = SigningKey.SupervisorPublicKey
    #usPublickey = S
    
    #signature = supPublicKey.sign(b"FinalProject")
    
    #print(signature)
    
    #public_key = UserPublicKey.verifying_key
    #print("Verified:", public_key.verify(signature, b"FinalProject"))

    #verify purchase orderhash order using thep public of the user hash

    #public key say pkcsa1.15. new

from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_v1_5, DES
import rsa

def depart():
     
    # var1 = rsa.
    # var2 = rsa.signMessage()
    # print(var2)

    print("Verifying signature...")
    try:
            #get the user key              create private cipher
        pkcs1_15.new(rsa.self.key).verify(rsa.messageHash, rsa.self.privateCipher.sign(messageHash))
    except ValueError:
        print("Error! Failed to verify signature")
        #conn.close()
        return
    
    print("Signature verified, initating session key ")
    
    # we will call this funcation FulfillOrder()



