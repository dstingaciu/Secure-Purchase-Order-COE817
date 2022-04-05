import socket
from org_key_server import key_server
from org_add_purchase_order import retrieveLatestPurchaseOrderRequests
from org_employees import Supervisor, deptEmployee
from rsa import rsaKeyServer

new_key_gen = rsaKeyServer()

ksi = key_server(new_key_gen)

while(True):
    # Setup connection socket
    s = socket.socket()
    port = 60000
    host = socket.gethostname()
    s.bind(('127.0.0.1', port))     # Bind to the port
    s.listen(5)                     # Now wait for client connection

    print("await connection from client...")

    # Await connection from a client
    conn, addr = s.accept()

    ksi.initConnection(conn)

    print("Press enter to go to the next step...")
    nextStep = input()

    RLPOR = retrieveLatestPurchaseOrderRequests(new_key_gen).retrieveEncryptedPO()
    
    print("Done adding purchase order to db...")

    print("Enter supervisor name: ")
    supervisor_name = input()

    newSuper = Supervisor(supervisor_name)
    newSuper.initSupervisorFlow()

    print("Enter department employee name: ")
    deptName = input()

    newEmployee = deptEmployee(deptName, newSuper.getPublicSuperKey().decode()).initDepartmentFlow()

    s.close()

    print("Exit? (1 for yes, 0 for no): ")
    exitCmd = input()

    if(exitCmd == "1"):
        exit(1)



    