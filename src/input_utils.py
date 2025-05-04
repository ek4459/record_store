from typing import Optional, Dict, Any, Callable
from crud_operations import handle_lookup

def get_input(prompt: str, existing_value: Any = None, validation_func: Callable = None, is_update: bool = False) -> Any:
    while True:
        try:
            if is_update and existing_value is not None:
                value = input(f"{prompt} [{existing_value}]: ").strip()
                if not value:
                    return existing_value
            else:
                value = input(f"{prompt}: ").strip()
                if not value:
                    print("This field is required.")
                    continue
            if validation_func:
                return validation_func(value)
            return value
        except ValueError as e:
            print(f"Invalid input: {str(e)}")

def get_record_id(table_name: Optional[str] = None) -> Optional[int]:
    while True:
        try:
            prompt = f"Enter {table_name} ID (or 'b' to go back): " if table_name else "Enter record ID (or 'b' to go back): "
            user_input = input(prompt).strip().lower()
            
            if user_input == 'b':
                return None
                
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number or 'b' to go back.")

def get_customer_data(connection, existing_customer: Dict[str, Any] = None) -> Dict[str, Any]:
    is_update = existing_customer is not None
    print("\nEnter Customer Details" + (" (leave blank to keep existing value):" if is_update else ":"))
    data = {}
    
    data["FirstName"] = get_input("First Name", existing_customer["FirstName"] if existing_customer else None, is_update=is_update)
    data["LastName"] = get_input("Last Name", existing_customer["LastName"] if existing_customer else None, is_update=is_update)
    data["Email"] = get_input("Email", existing_customer["Email"] if existing_customer else None, is_update=is_update)
    data["Phone"] = get_input("Phone (XXX-XXX-XXXX)", existing_customer["Phone"] if existing_customer else None, is_update=is_update)
    data["BirthDate"] = get_input("Birth Date (YYYY-MM-DD)", existing_customer["BirthDate"] if existing_customer else None, is_update=is_update)
    
    data["GenreID"] = handle_lookup(
        connection,
        "Genre",
        "GenreID",
        "GenreName",
        existing_customer["GenreID"] if existing_customer else None,
        None,
        "Preferred Genre"
    )
    
    return {k: v for k, v in data.items() if v is not None}

def get_band_data(connection, existing_band: Dict[str, Any] = None) -> Dict[str, Any]:
    is_update = existing_band is not None
    print("\nEnter Band Details" + (" (leave blank to keep existing value):" if is_update else ":"))
    data = {}
    
    data["BandName"] = get_input("Band Name", existing_band["BandName"] if existing_band else None, is_update=is_update)
    data["FoundedYear"] = get_input("Founded Year", existing_band["FoundedYear"] if existing_band else None, is_update=is_update)
    data["Country"] = get_input("Country", existing_band["Country"] if existing_band else None, is_update=is_update)
    
    data["GenreID"] = handle_lookup(
        connection,
        "Genre",
        "GenreID",
        "GenreName",
        existing_band["GenreID"] if existing_band else None,
        None,
        "Genre"
    )
    
    data["RecordLabelID"] = handle_lookup(
        connection,
        "Record_Label",
        "RecordLabelID",
        "LabelName",
        existing_band["RecordLabelID"] if existing_band else None,
        None,
        "Record Label"
    )
    
    return {k: v for k, v in data.items() if v is not None}

def get_album_data(connection, existing_album: Dict[str, Any] = None) -> Dict[str, Any]:
    is_update = existing_album is not None
    print("\nEnter Album Details" + (" (leave blank to keep existing value):" if is_update else ":"))
    data = {}
    
    data["Title"] = get_input("Title", existing_album["Title"] if existing_album else None, is_update=is_update)
    data["ReleaseDate"] = get_input("Release Date (YYYY-MM-DD)", existing_album["ReleaseDate"] if existing_album else None, is_update=is_update)
    data["Price"] = get_input("Price", existing_album["Price"] if existing_album else None, is_update=is_update)
    data["Format"] = get_input("Format (Vinyl/CD/Cassette/Digital)", existing_album["Format"] if existing_album else None, is_update=is_update)
    
    data["BandID"] = handle_lookup(
        connection,
        "Band",
        "BandID",
        "BandName",
        existing_album["BandID"] if existing_album else None,
        None,
        "Band"
    )
    
    return {k: v for k, v in data.items() if v is not None}

def get_genre_data(connection, existing_genre: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    is_update = existing_genre is not None
    print("\nEnter Genre Details" + (" (leave blank to keep existing value):" if is_update else ":"))
    data = {}
    
    data["GenreName"] = get_input("Genre Name", existing_genre["GenreName"] if existing_genre else None, is_update=is_update)
    data["Description"] = get_input("Description (optional)", existing_genre["Description"] if existing_genre else None, is_update=is_update)
    
    return {k: v for k, v in data.items() if v is not None}

def get_record_label_data(connection, existing_label: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    is_update = existing_label is not None
    print("\nEnter Record Label Details" + (" (leave blank to keep existing value):" if is_update else ":"))
    data = {}
    
    data["LabelName"] = get_input("Label Name", existing_label["LabelName"] if existing_label else None, is_update=is_update)
    data["FoundedYear"] = get_input("Founded Year (optional)", existing_label["FoundedYear"] if existing_label else None, is_update=is_update)
    data["Country"] = get_input("Country (optional)", existing_label["Country"] if existing_label else None, is_update=is_update)
    
    return {k: v for k, v in data.items() if v is not None} 
