import sqlite3

def get_all_tables_and_columns(db_path: str):
    """Connect to a SQLite database and retrieve all tables, columns, and their data types."""
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return None

    # Get columns and data types for each table
    table_info = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [(col[1], col[2]) for col in cursor.fetchall()]  # (column_name, data_type)
        table_info[table] = columns

    # Close connection
    conn.close()

    # Print tables, columns, and data types
    print("\n📌 **Tables, Columns, and Data Types:**")
    for table, columns in table_info.items():
        print(f"🔹 Table: {table}")
        for column, datatype in columns:
            print(f"    - {column}: {datatype}")

    # Convert to Pandas DataFrame

# 🔹 Run the script
if __name__ == "__main__":
    db_path = "huntil.db"  # Replace with your actual database file
    get_all_tables_and_columns(db_path)
