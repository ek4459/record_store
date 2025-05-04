from typing import List, Callable

from crud_operations import (
    add_record,
    update_record,
    delete_record,
    view_records,
    fetch_records
)
from order_operations import place_order, cancel_order
from input_utils import (
    get_customer_data,
    get_band_data,
    get_album_data,
    get_genre_data,
    get_record_label_data,
    get_record_id
)

def show_menu(title: str, options: List[str], is_main_menu: bool = False) -> str:
    print(f"\n{title}:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    if not is_main_menu:
        print(f"{len(options) + 1}. Return to previous menu")
    return input("\nEnter your choice: ")

def show_main_menu() -> str:
    return show_menu("Main Menu", [
        "Customer Management",
        "Band Management",
        "Album Management",
        "Order Management",
        "Genre Management",
        "Record Label Management",
        "Analytics",
        "Exit"
    ], is_main_menu=True)

def show_customer_menu() -> str:
    return show_menu("Customer Management", [
        "View Customers",
        "Add Customer",
        "Update Customer",
        "Delete Customer"
    ])

def show_band_menu() -> str:
    return show_menu("Band Management", [
        "View Bands",
        "Add Band",
        "Update Band",
        "Delete Band"
    ])

def show_album_menu() -> str:
    return show_menu("Album Management", [
        "View Albums",
        "Add Album",
        "Update Album",
        "Delete Album"
    ])

def show_order_menu() -> str:
    return show_menu("Order Management", [
        "Place Order",
        "View Orders",
        "Cancel Order"
    ])

def show_analytics_menu() -> str:
    """Display the analytics menu and return user's choice."""
    return show_menu("Analytics", [
        "View Sales by Genre",
        "View Band Performance",
        "View Customer Purchase History",
        "View Inventory Analysis"
    ])

def handle_crud_operations(connection, table_name: str, id_column: str, get_data_func: Callable) -> bool:
    menu_text = {
        "Customers": "Customers",
        "Band": "Bands",
        "Album": "Albums",
        "Genre": "Genres",
        "Record_Label": "Record Labels"
    }
    
    view_names = {
        "Customers": "vw_customers",
        "Band": "vw_bands",
        "Album": "vw_albums",
        "Genre": "vw_genres",
        "Record_Label": "vw_record_labels"
    }

    display_name = menu_text[table_name]
    
    choice = show_menu(f"{display_name} Management", [
        f"View {display_name}",
        f"Add {display_name}",
        f"Update {display_name}",
        f"Delete {display_name}"
    ])
    
    if choice == "1":
        view_records(connection, view_names[table_name])
        return True
    elif choice == "2":
        data = get_data_func(connection)
        add_record(connection, table_name, data)
        return True
    elif choice == "3":
        view_records(connection, view_names[table_name])
        
        record_id = get_record_id(display_name)
        if record_id is not None:
            columns, records = fetch_records(connection, table_name, f"{id_column} = {record_id}")
            if records:
                existing_record = dict(zip(columns, records[0]))
                data = get_data_func(connection, existing_record)
                update_record(connection, table_name, record_id, data, id_column=id_column)
        return True
    elif choice == "4":
        view_records(connection, view_names[table_name])
        
        record_id = get_record_id(display_name)
        if record_id is not None:
            delete_record(connection, table_name, record_id, id_column=id_column)
        return True
    elif choice == "5":
        return True
    else:
        print("Invalid choice. Please try again.")
        return True

def handle_analytics(connection) -> bool:
    choice = show_analytics_menu()
    view_mapping = {
        "1": "vw_sales_by_genre",
        "2": "vw_band_performance",
        "3": "vw_customer_purchase_history",
        "4": "vw_inventory_analysis"
    }
    
    if choice in view_mapping:
        if view_mapping[choice] is None:
            return True
        view_records(connection, view_mapping[choice])
        return True
    return True 

def handle_order_menu(connection) -> bool:
    choice = show_order_menu()
    if choice == "1":
        return place_order(connection)
    elif choice == "2":
        view_records(connection, "vw_order_details")
        
        order_id = get_record_id("Order")
        if order_id is not None:
            view_records(connection, "vw_order_items", f"OrderID = {order_id}")
        return True
    elif choice == "3":
        view_records(connection, "vw_order_details")
        order_id = get_record_id("Order")
        if order_id is not None:
            return cancel_order(connection, order_id)
        return True
    else:
        print("Invalid choice. Please try again.")
        return True

def handle_menu_choice(connection, choice: str) -> bool:
    menu_handlers = {
        "1": lambda: handle_crud_operations(connection, "Customers", "CustomerID", get_customer_data),
        "2": lambda: handle_crud_operations(connection, "Band", "BandID", get_band_data),
        "3": lambda: handle_crud_operations(connection, "Album", "AlbumID", get_album_data),
        "4": lambda: handle_order_menu(connection),
        "5": lambda: handle_crud_operations(connection, "Genre", "GenreID", get_genre_data),
        "6": lambda: handle_crud_operations(connection, "Record_Label", "RecordLabelID", get_record_label_data),
        "7": lambda: handle_analytics(connection),
        "8": lambda: False
    }
    
    if choice in menu_handlers:
        return menu_handlers[choice]()
    else:
        print("Invalid choice. Please try again.")
        return True 
