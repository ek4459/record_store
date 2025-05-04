from database import connect_to_database
from menu_functions import show_main_menu, handle_menu_choice

def main():
    print("Welcome to the Record Store Management System!")
    
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to database. Exiting...")
        return
    
    try:
        while True:
            try:
                choice = show_main_menu()
                if not handle_menu_choice(connection, choice):
                    break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again.")
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main() 
