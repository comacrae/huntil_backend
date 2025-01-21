import sqlite3

def migrate_harvest(db_path: str):
    """ Migrates the SQLite database to add a primary key to the harvest table. """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        # 1. Create a new table with the correct primary key
        cursor.execute("""
            CREATE TABLE harvest_new (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id TEXT NOT NULL,
                site TEXT NOT NULL,
                year INT NOT NULL,
                species TEXT NOT NULL,
                season TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                harvest_count INTEGER
            )
        """)
        
        # 2. Copy existing data into the new table
        cursor.execute("""
            INSERT INTO harvest_new (site_id, site, year, species, season, subcategory, harvest_count)
            SELECT site_id, site, year, species, season, subcategory, harvest_count FROM harvest;
        """)
        
        # 3. Drop the old table
        cursor.execute("DROP TABLE harvest;")
        
        # 4. Rename the new table to match the original table name
        cursor.execute("ALTER TABLE harvest_new RENAME TO harvest;")
        
        # Commit the changes
        connection.commit()
        print("Database migration completed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def migrate_huntable_species(db_path: str):
    """ Migrates the SQLite database to add a primary key to the harvest table. """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        # 1. Create a new table with the correct primary key
        cursor.execute("""
            CREATE TABLE huntable_species_new (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id TEXT NOT NULL,
                species TEXT NOT NULL,
                season TEXT NOT NULL,
                stipulation TEXT NOT NULL
            )
        """)
        
        # 2. Copy existing data into the new table
        cursor.execute("""
            INSERT INTO huntable_species_new ( site_id, species, season, stipulation)
            SELECT  site_id,species, season, stipulation FROM huntable_species;
        """)
        
        # 3. Drop the old table
        cursor.execute("DROP TABLE huntable_species;")
        
        # 4. Rename the new table to match the original table name
        cursor.execute("ALTER TABLE huntable_species_new RENAME TO huntable_species;")
        
        # Commit the changes
        connection.commit()
        print("Database migration completed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Example usage
if __name__ == "__main__":
    migrate_harvest("./huntil.db")
    migrate_huntable_species("./huntil.db")
