from src.data.scripts.create_db import create_db
from src.utils.generator import create_record
# from src.new_insert import main as insert_initial_data
from validate_and_load_records import main as insert_initial_data

def main():
    create_record()          # si genera datos previos
    create_db()              # crea y limpia la base
    insert_initial_data()    # inserta projects y devices

if __name__ == "__main__":
    main()
