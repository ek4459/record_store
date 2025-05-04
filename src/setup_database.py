import os
import re
import keyring

from database import set_database_password, connect_to_database

def main():
    print("Database Setup")
    print("=============")
    print("This script will help you set up your database password in the system keyring.")
    print("The password will be securely stored and used by the application.")
    print("\nNote: This only needs to be done once.")
    
    try:
        keyring.delete_password('record_store_db', 'root')
        print("Cleared existing database password from keyring.")
    except keyring.errors.PasswordDeleteError:
        print("No existing password found in keyring.")
    
    set_database_password()
    
    connection = connect_to_database(create_db=True)
    if not connection:
        print("Failed to connect to MySQL. Please check your credentials.")
        return
        
    try:
        cursor = connection.cursor()
        

        print("\nCreating database...")
        cursor.execute("DROP DATABASE IF EXISTS my_record_shop")
        cursor.execute("CREATE DATABASE my_record_shop")
        cursor.execute("USE my_record_shop")
        

        print("Setting up database schema...")
        sql_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'My_Record_Store.sql')
        with open(sql_file, 'r') as file:
            sql_script = file.read()
            
        statements = []
        current_statement = ""
        delimiter = ";"
        
        for line in sql_script.split('\n'):

            if line.strip().upper().startswith('DELIMITER'):
                delimiter = line.strip().split()[1]
                continue
                
            current_statement += line + "\n"
            
            if line.strip().endswith(delimiter) and not re.search(r'(CREATE\s+(PROCEDURE|FUNCTION|TRIGGER))', current_statement, re.IGNORECASE):
                statements.append(current_statement)
                current_statement = ""
        
        if current_statement.strip():
            statements.append(current_statement)
            
        for statement in statements:
            if statement.strip():
                try:
                    is_complex = bool(re.search(r'(CREATE\s+(PROCEDURE|FUNCTION|TRIGGER))', statement, re.IGNORECASE))
                    
                    if is_complex:
                        for result in cursor.execute(statement, multi=True):
                            if result.with_rows:
                                result.fetchall()
                    else:
                        cursor.execute(statement)
                    
                    connection.commit()
                except Exception as e:
                    print(f"Error executing statement: {e}")
                    print(f"Statement: {statement[:100]}...")
                    raise
                
        print("\nSetup complete! Database has been created and initialized.")
        print("You can now run the main application.")
        
    except Exception as e:
        print(f"Error during database setup: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main() 
