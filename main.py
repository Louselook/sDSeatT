from src.data.scripts.create_db import create_db
from src.utils.generator import create_record
from app import run_server
import os
from src.utils import *

def main():
    os.makedirs("src/data/db", exist_ok=True)
    create_record()          # si genera datos previos
    create_db()              # crea y limpia la base
    insert_initial_data()    # inserta projects y devices
    run_server()

if __name__ == "__main__":
    main()
