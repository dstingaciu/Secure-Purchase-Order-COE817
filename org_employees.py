import ast
from unicodedata import name
from rsa import rsaKeyServer
from email_access import accessEmail
from org_helpers import fulfillPurchaseOrder, insertSuperSig, retrievePurchaseOrder, retrieveSignedUnfulfilledPurchaseOrder
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

class Supervisor():
    def __init__(self, name):
        self.name = name
        self.superKey = rsaKeyServer()
        print("Welcome "+name)

    def initSupervisorFlow(self):
        done = 0
        while(done == 0):
            self.__printSuperMenu()
            print("Enter a commmand: ")
            cmd = input()

            if(cmd == "1"):
                self.retrieveOrders()
            elif(cmd == "2"):
                self.__printSuperMenu()
            elif(cmd == "3"):
                done = 1
            else:
                print("Invalid command...")
                

    def retrieveOrders(self):
        orderTuple = retrievePurchaseOrder()
        if(len(orderTuple) > 0):
            pon, email, PO, u_sig, s_sig, fulfilled, sec_flag, sid = orderTuple[0]
            print("Here's the latest order: ")
            print(PO)
            if(sec_flag == 0):
                print("The user purchase order is VERIFIED")
            else:
                print("The user purchase order has RAISED A SECURITY FLAG")
            print("Do you approve of this order (1 for yes, 0 for no): ")
            approval = input()
            if(approval == "1"):
                SupervisorSignature, digest = self.superKey.signMessage(str.encode(PO))
                strSSig = f"{SupervisorSignature}"
                insertSuperSig(pon, strSSig)
                print("APPROVED!")
            else:
                print("NOT APPROVED")
        else:
            print("No more orders!")


    def getPublicSuperKey(self):
        return self.superKey.key.public_key().export_key()

    def __printSuperMenu(self):
        print("Here's a list of commands:")
        print("1) Retrieve latest unsigned order")
        print("2) Relist commands")
        print("3) Exit supervisor screen")


class deptEmployee():
    def __init__(self,name, PU):
        self.name = name
        self.superPublic = PU
    
    def initDepartmentFlow(self):
        done = 0
        while(done == 0):
            self.__printDeptMenu()
            print("Enter a commmand: ")
            cmd = input()

            if(cmd == "1"):
                self.retrieveOrders()
            elif(cmd == "2"):
                self.__printDeptMenu()
            elif(cmd == "3"):
                done = 1
            else:
                print("Invalid command...")

    def retrieveOrders(self):
        orderTuple = retrieveSignedUnfulfilledPurchaseOrder()
        if(len(orderTuple) > 0):
            pon, email, PO, u_sig, s_sig, fulfilled, sec_flag, sid = orderTuple[0]

            print("Here's the latest order: ")
            print(PO)

            if(sec_flag == 0):
                print("The user purchase order is VERIFIED")
            else:
                print("The user purchase order has RAISED A SECURITY FLAG")

            print("Can you fulfill this order? (1 for yes, 0 for no): ")
            response = input()

            if(response == "1"):
                print("Verifiying the supervisor signature...")
                signedOrderHashLiteral = ast.literal_eval(s_sig)
                superRSA = RSA.import_key(self.superPublic)
                hashedPO = SHA256.new(str.encode(PO))
                try:
                    pkcs1_15.new(superRSA).verify(hashedPO, signedOrderHashLiteral)
                    print("Supervisor signature verified!")
                    fulfillPurchaseOrder(int(pon))
                except Exception as ex:
                    print("Error! Failed to verify supervisor signature")
                    print(ex)
        else:
            print("No more orders!")


    def __printDeptMenu(self):
        print("Here's a list of commands:")
        print("1) Retrieve latest signed orders")
        print("2) Relist commands")
        print("3) Exit supervisor screen")