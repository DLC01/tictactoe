import json

config_filename = "config.json"

def create_config_file():
    user=input("enter the username")
    passw=input"enter the password")
    db=input("enter the database name")
    config_data = {
    "username": user,
    "password": passw,
    "database": db,
    }

    global config_filename

    # Write the data to the JSON file
    with open(config_filename, "w") as config_file:
        json.dump(config_data, config_file)

def open_config_file():
    global config_filename
    try:
        # Attempt to open and read the JSON file
        with open(config_filename, "r") as config_file:
            config_data = json.load(config_file)

            username = config_data["username"]
            password = config_data["password"]
            database = config_data["database"]
    except FileNotFoundError:
        print("Config file not found")
    
    return username,password,database

