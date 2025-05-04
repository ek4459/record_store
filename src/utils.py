def format_table(headers, rows):
    col_widths = [
        max(len(str(header)), max(len(str(row[i])) for row in rows))
        for i, header in enumerate(headers)
    ]
    
    format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
    
    separator = "-+-".join("-" * width for width in col_widths)
    
    table_str = "\n" + format_str.format(*headers) + "\n"
    table_str += separator + "\n"
    for row in rows:
        table_str += format_str.format(*row) + "\n"
    table_str += separator + "\n"
    table_str += f"Total records: {len(rows)}\n"
    
    return table_str 
