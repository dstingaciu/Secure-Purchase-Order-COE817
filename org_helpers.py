import sqlite3

"""SESSION KEY QUERIES"""

# Adds session keys to the database
def addToSessionKeys(email, s_key_str):
    s_table_values = (email, s_key_str)
    try:
        # Connect to DB
        con = sqlite3.connect("org.db")

        # Prepare INSERT statement for session_key table with given email and session key string
        con.execute(""" 
            INSERT INTO session_keys (email, s_key) VALUES (?, ?)
        """, s_table_values)

        # Commit statement
        con.commit()

        # Close DB connection
        con.close()
        return True
    except Exception as ex:
        print("Error adding session to DB!")
        print(ex)
    
    return False

# Retrieves ALL session keys from user
def retrieveStoredSessionKey(email):
    s_table_values = (email,)
    try:
        # Connect to DB
        con = sqlite3.connect("org.db")

        # Retrieve session keys for email from database
        res = con.execute("SELECT s_key FROM session_keys WHERE email LIKE ?", s_table_values)

        # Assign to array
        rVal = res.fetchall()

        # Close DB connection
        con.close()

        # Return array with all session keys
        return rVal
    except:
        print("Error connecting to db...")
        return None

# Delete Session key with session key
def deleteFromSessionKeyWithSKey(s_key):
    s_table_values = (s_key,)
    try:
        # Connect to DB
        con = sqlite3.connect("org.db")

        # Prepare INSERT statement for session_key table with given email and session key string
        con.execute(""" 
            DELETE FROM session_keys WHERE s_key LIKE ?
        """, s_table_values)

        # Commit statement
        con.commit()

        # Close DB connection
        con.close()
        return True
    except Exception as ex:
        print("Error adding session to DB!")
        print(ex)
    
    return False

# Delete Session key with email
def deleteFromSessionKeyWitEmail(email):
    s_table_values = (email,)
    try:
        # Connect to DB
        con = sqlite3.connect("org.db")

        # Prepare INSERT statement for session_key table with given email and session key string
        con.execute(""" 
            DELETE FROM session_keys WHERE email LIKE ?
        """, s_table_values)

        # Commit statement
        con.commit()

        # Close DB connection
        con.close()
        return True
    except Exception as ex:
        print("Error adding session to DB!")
        print(ex)
    
    return False

"""PURCHASE ORDER QUERIES"""
# Adds session keys to the database
def addToPurchaseOrderFromClient(email, PO_str, user_sig):
    po_table_values = (email, PO_str, user_sig)
    try:
        # Connect to DB
        con = sqlite3.connect("org.db")

        # Prepare INSERT statement for session_key table with given email and session key string
        con.execute(""" 
            INSERT INTO purchase_orders (email, PO, u_sig, fulfilled, sec_flag) VALUES (?, ?, ?, 0, 0)
        """, po_table_values)

        # Commit statement
        con.commit()

        # Close DB connection
        con.close()
        return True
    except Exception as ex:
        print("Error adding session to DB!")
        print(ex)
    
    return False

# Retrieve Purchase Order
def retrievePurchaseOrder():
    # Retrieves ALL unfulfilled POs from user
    try:
        # Connect to DB
        con = sqlite3.connect("org.db")

        # Retrieve session keys for email from database
        res = con.execute("SELECT * FROM purchase_orders")

        # Assign to array
        rVal = res.fetchall()

        # Close DB connection
        con.close()

        # Return array with all session keys
        return rVal
    except:
        print("Error connecting to db...")
        return None