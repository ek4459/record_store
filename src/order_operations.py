from typing import Optional
from database import transaction
from crud_operations import add_record, update_record, fetch_records, view_records
from input_utils import get_record_id

def get_payment_method() -> Optional[str]:
    while True:
        print("\nSelect Payment Method:")
        print("1. Credit Card")
        print("2. PayPal")
        print("3. Cash")
        print("4. Go Back")
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == '4' or choice == 'b':
            return None
            
        return {
            "1": "Credit Card",
            "2": "PayPal",
            "3": "Cash"
        }.get(choice, "Credit Card")

def cancel_order(connection, order_id: int) -> bool:
    try:
        with transaction(connection, 'SERIALIZABLE') as cursor:
            success = update_record(connection, "Orders", order_id, {'OrderStatus': 'Cancelled'}, 'OrderID')
            if not success:
                print("\nFailed to update order status.")
                return True

            cursor.callproc('sp_remove_loyalty_points', (
                order_id,  
                False,     
                ''         
            ))
            
            for result in cursor.stored_results():
                success, message = result.fetchone()
                print(f"\n{message}")
                if success:
                    print("\nCancelled Order Summary:")
                    view_records(connection, "vw_order_summary", f"OrderID = {order_id}")
                    print("\nOrder Items:")
                    view_records(connection, "vw_order_items", f"OrderID = {order_id}")
                return True
            return True
    except Exception as e:
        print(f"Error cancelling order: {e}")
        return True

def place_order(connection) -> bool:
    try:
        print("\nAvailable Customers:")
        view_records(connection, "vw_customers")
        customer_id = get_record_id("Customers")
        if not customer_id:
            return True
            
        columns, records = fetch_records(connection, "Customers", f"CustomerID = {customer_id}")
        if not records:
            print("\nCustomer not found. Please try again.")
            return True
            
        payment_method = get_payment_method()
        if not payment_method:
            return True
            
        with transaction(connection, 'SERIALIZABLE') as cursor:
            order_data = {
                'CustomerID': customer_id,
                'OrderDate': 'NOW()',
                'PaymentMethod': payment_method,
                'OrderStatus': 'Pending'
            }
            order_id = add_record(connection, "Orders", order_data)
            if not order_id:
                print("\nFailed to create order.")
                return True
            
        print("\nAvailable Albums:")
        view_records(connection, "vw_albums")
        
        while True:
            print("\nAdd items to order:")
            print("1. Add an album")
            print("2. Complete order")
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == '1':
                album_id = get_record_id("Album")
                if not album_id:
                    continue
                    
                try:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Quantity must be greater than 0.")
                        continue
                except ValueError:
                    print("Invalid quantity. Please enter a number.")
                    continue
                
                with transaction(connection, 'SERIALIZABLE') as cursor:
                    columns, records = fetch_records(connection, "Album", f"AlbumID = {album_id}")
                    if not records:
                        print("\nAlbum not found. Please try again.")
                        continue
                    album_price = records[0][columns.index('Price')]
                    
                    order_line_data = {
                        'OrderID': order_id,
                        'AlbumID': album_id,
                        'Quantity': quantity,
                        'UnitPrice': album_price
                    }
                    if not add_record(connection, "Order_Line", order_line_data):
                        print("\nFailed to add order line.")
                        continue
                    
                    print("\nAlbum added to order successfully.")
                    
            elif choice == '2':
                with transaction(connection, 'SERIALIZABLE') as cursor:
                    success = update_record(connection, "Orders", order_id, {'OrderStatus': 'Processing'}, 'OrderID')
                    if not success:
                        print("\nFailed to complete order.")
                        continue
                    
                    print("\nOrder completed successfully.")
                    print("\nOrder Summary:")
                    view_records(connection, "vw_order_summary", f"OrderID = {order_id}")
                    print("\nOrder Items:")
                    view_records(connection, "vw_order_items", f"OrderID = {order_id}")
                    return True
                    
    except Exception as e:
        print(f"Error placing order: {e}")
        return True
