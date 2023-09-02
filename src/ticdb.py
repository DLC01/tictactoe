import mysql.connector
import src.ticdata as ticdata
import os

# Connect to MySQL database
def manage_db():
    file_path = "config.dat"

    if os.path.exists(file_path):
        print("Config file found, Loading...")
        db_username,db_password,db_database=ticdata.open_config_file()
    else:
        print("Config file not found, Creating one...")
        ticdata.create_config_file()
        db_username,db_password,db_database=ticdata.open_config_file()

    try:
        db = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host="localhost",
            database=db_database
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to Database: {e}")
        exit(1)

    # Get Cursor
    cursor = db.cursor()

    # Remove existing tables(if any)
    cursor.execute("DROP TABLE IF EXISTS scores")
    db.commit

    # Create table if it doesnt exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS scores (
        player_name VARCHAR(255) PRIMARY KEY,
        wins INT
    )   
    """
    cursor.execute(create_table_sql)
    db.commit()

    return cursor, db
