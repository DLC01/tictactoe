import mysql.connector
import sys
import ticdata
import os

# Connect to MySQL database
def manage_db():
    file_path = "config.json"

    if os.path.exists(file_path):
        db_username,db_password,db_database=open_config_file()
    else:
        create_config_file()

    try:
        db = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host="localhost",
            database=db_database
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to Database: {e}")
        sys.exit(1)

    # Get Cursor
    cursor = db.cursor()

    #create table if it doesnt exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tic_tac_toe_scores (
        player_name VARCHAR(255) PRIMARY KEY,
        wins INT
    )   
    """
    cursor.execute(create_table_sql)
    db.commit()

