from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error
import keyring

ISOLATION_LEVELS = {
    'READ_UNCOMMITTED': 'READ UNCOMMITTED',
    'READ_COMMITTED': 'READ COMMITTED',
    'REPEATABLE_READ': 'REPEATABLE READ',
    'SERIALIZABLE': 'SERIALIZABLE'
}

def connect_to_database(create_db=False, isolation_level=None):
    try:
        print("Attempting to connect to MySQL...")
        
        password = keyring.get_password('record_store_db', 'root')
        if not password:
            print("No password found in keyring. Please set the password first.")
            return None
            
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="my_record_shop" if not create_db else None,
            auth_plugin='mysql_native_password'
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            if isolation_level:
                set_isolation_level(connection, isolation_level)
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        print(f"Error code: {e.errno}")
        print(f"SQL state: {e.sqlstate}")
        return None

def set_isolation_level(connection, level):
    try:
        if level not in ISOLATION_LEVELS:
            raise ValueError(f"Invalid isolation level. Must be one of: {list(ISOLATION_LEVELS.keys())}")
        
        cursor = connection.cursor()
        cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {ISOLATION_LEVELS[level]}")
        connection.commit()
        print(f"Isolation level set to: {ISOLATION_LEVELS[level]}")
    except Error as e:
        print(f"Error setting isolation level: {e}")
        raise

@contextmanager
def transaction(connection, isolation_level='REPEATABLE_READ', debug=False):
    cursor = connection.cursor()
    is_nested = connection.in_transaction
    
    try:
        if not is_nested:
            cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {ISOLATION_LEVELS[isolation_level]}")
            if debug:
                print(f"Transaction started with {isolation_level} isolation level")
        else:
            if debug:
                print("Nested transaction started, inheriting parent's isolation level")
        
        yield cursor
        
        if not is_nested:
            connection.commit()
            if debug:
                print("Transaction committed successfully")
            
    except Exception as e:
        if not is_nested:
            connection.rollback()
            if debug:
                print("Transaction rolled back due to error")
        raise e
    finally:
        cursor.close()

def execute_transaction(connection, query, params=None, isolation_level=None):
    with transaction(connection, isolation_level) as cursor:
        cursor.execute(query, params or ())
        if cursor.with_rows:
            return cursor.fetchall()
        return cursor.rowcount

def set_database_password():
    password = input("Enter the database password: ")
    keyring.set_password('record_store_db', 'root', password)
    print("Password stored in keyring successfully!") 