from typing import List, Dict, Any, Optional, Tuple

from database import transaction
from utils import format_table


def fetch_records(connection, table_name: str, where_clause: str = None, params: tuple = None, isolation_level='READ_COMMITTED') -> Tuple[List[str], List[tuple]]:
    """Fetch records from a table and return column names and records."""
    try:
        with transaction(connection, isolation_level) as cursor:
            query = f"SELECT * FROM {table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            cursor.execute(query, params or ())
            columns = [desc[0] for desc in cursor.description]
            records = cursor.fetchall()
            return columns, records
    except Exception as e:
        print(f"Error fetching records: {e}")
        return [], []

def view_records(connection, view_name: str, where_clause: str = None, isolation_level='READ_COMMITTED') -> bool:
    """Display records from a view with optional filtering."""
    try:
        with transaction(connection, isolation_level) as cursor:
            query = f"SELECT * FROM {view_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                # Convert records to strings and handle None values
                formatted_records = [
                    tuple(str(val) if val is not None else "N/A" for val in record)
                    for record in records
                ]
                # Get column names from cursor description
                columns = [desc[0] for desc in cursor.description]
                print(format_table(columns, formatted_records))
                return True
            else:
                print("\nNo records found.")
                return False
    except Exception as e:
        print(f"\nError viewing records: {str(e)}")
        return False

# Function to add a new record to a table
def add_record(connection, table_name: str, data: Dict[str, Any], isolation_level='READ_COMMITTED'):
    """Add a new record using transaction management"""
    try:
        with transaction(connection, isolation_level) as cursor:
            # Build the column list and value placeholders
            columns = []
            values = []
            params = []
            
            for key, value in data.items():
                columns.append(key)
                if isinstance(value, str) and value.endswith('()'):  # SQL function
                    values.append(value)  # Use the function directly
                else:
                    values.append('%s')
                    params.append(value)
            
            # Build and execute the INSERT query
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"
            cursor.execute(query, params)
            
            # Get the ID of the newly inserted record
            if cursor.lastrowid:
                return cursor.lastrowid
            return True
    except Exception as e:
        error_msg = str(e)
        print(f"\nError adding record: {error_msg}")
        return False

# Function to update an existing record
def update_record(connection, table_name: str, record_id: int, data: Dict[str, Any], id_column='ID', isolation_level='READ_COMMITTED'):
    """Update a record using transaction management"""
    try:
        with transaction(connection, isolation_level) as cursor:
            # Build the SET clause
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            
            # Build and execute the UPDATE query
            query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
            params = list(data.values()) + [record_id]
            cursor.execute(query, params)
            
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating record: {e}")
        return False

# Function to delete a record
def delete_record(connection, table_name: str, record_id: int, id_column='ID', isolation_level='READ_COMMITTED'):
    """Delete a record using transaction management"""
    try:
        with transaction(connection, isolation_level) as cursor:
            query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
            cursor.execute(query, (record_id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting record: {e}")
        return False

def handle_lookup(connection, table_name: str, id_column: str, name_column: str, 
                 current_id: Optional[int], current_name: Optional[str], 
                 prompt: str) -> Optional[int]:
    if current_id:
        columns, records = fetch_records(connection, table_name, f"{id_column} = {current_id}")
        if records:
            current_name = records[0][columns.index(name_column)]
    
    while True:
        # Only show brackets if there's a current value
        input_prompt = f"{prompt} [{current_name}]" if current_name else f"{prompt}"
        name = input(f"{input_prompt}: ").strip()
        if not name:
            return current_id
            
        columns, records = fetch_records(connection, table_name, f"{name_column} = '{name}'")
        if records:
            return records[0][columns.index(id_column)]
            
        print(f"\nError: The {table_name.lower()} '{name}' does not exist. Please add it first or enter another value.") 