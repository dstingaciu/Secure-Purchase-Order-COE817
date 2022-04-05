from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from rsa import rsaKeyServer
from email_access import accessEmail
import socket
import time
import json

class Supervisor():
    def __init__(self, name):
        self.name = name
        print("Welcome "+name)

    def __retrieveLatestOrder():
        return accessEmail()

    def __printSuperMenu():
        print("Here's a list of commands:")
        print("1) ")


