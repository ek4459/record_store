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
    
    # Clear any existing password in keyring
    try:
        keyring.delete_password('record_store_db', 'root')
        print("Cleared existing database password from keyring.")
    except keyring.errors.PasswordDeleteError:
        print("No existing password found in keyring.")
    
    # Set the database password
    set_database_password()
    
    # Connect to MySQL (without database)
    connection = connect_to_database(create_db=True)
    if not connection:
        print("Failed to connect to MySQL. Please check your credentials.")
        return
        
    try:
        cursor = connection.cursor()
        
        # Create database
        print("\nCreating database...")
        cursor.execute("DROP DATABASE IF EXISTS my_record_shop")
        cursor.execute("CREATE DATABASE my_record_shop")
        cursor.execute("USE my_record_shop")
        
        # Read and execute SQL script
        print("Setting up database schema...")
        sql_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'My_Record_Store.sql')
        with open(sql_file, 'r') as file:
            sql_script = file.read()
            
        # Split the script into statements, handling stored procedures and triggers
        statements = []
        current_statement = ""
        delimiter = ";"
        
        for line in sql_script.split('\n'):
            # Check for delimiter changes
            if line.strip().upper().startswith('DELIMITER'):
                delimiter = line.strip().split()[1]
                continue
                
            # Add line to current statement
            current_statement += line + "\n"
            
            # If we hit the delimiter and we're not in a stored procedure/trigger
            if line.strip().endswith(delimiter) and not re.search(r'(CREATE\s+(PROCEDURE|FUNCTION|TRIGGER))', current_statement, re.IGNORECASE):
                statements.append(current_statement)
                current_statement = ""
        
        # Add any remaining statement
        if current_statement.strip():
            statements.append(current_statement)
            
        # Execute each statement
        for statement in statements:
            if statement.strip():
                try:
                    # Check if this is a stored procedure, function, or trigger
                    is_complex = bool(re.search(r'(CREATE\s+(PROCEDURE|FUNCTION|TRIGGER))', statement, re.IGNORECASE))
                    
                    if is_complex:
                        # For complex statements, use multi=True
                        for result in cursor.execute(statement, multi=True):
                            if result.with_rows:
                                result.fetchall()
                    else:
                        # For simple statements, execute normally
                        cursor.execute(statement)
                    
                    # Commit after each statement
                    connection.commit()
                except Exception as e:
                    print(f"Error executing statement: {e}")
                    print(f"Statement: {statement[:100]}...")  # Print first 100 chars of problematic statement
                    raise
                
        print("\nSetup complete! Database has been created and initialized.")
        print("You can now run the main application.")
        
    except Exception as e:
        print(f"Error during database setup: {e}")
        connection.rollback()  # Rollback on error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main() 