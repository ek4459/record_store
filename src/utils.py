def format_table(headers, rows):
    """Format a table with consistent column widths and alignment"""
    # Calculate column widths based on both headers and data
    col_widths = [
        max(len(str(header)), max(len(str(row[i])) for row in rows))
        for i, header in enumerate(headers)
    ]
    
    # Create format string for each column
    format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
    
    # Create separator line
    separator = "-+-".join("-" * width for width in col_widths)
    
    # Build the formatted table string
    table_str = "\n" + format_str.format(*headers) + "\n"
    table_str += separator + "\n"
    for row in rows:
        table_str += format_str.format(*row) + "\n"
    table_str += separator + "\n"
    table_str += f"Total records: {len(rows)}\n"
    
    return table_str 