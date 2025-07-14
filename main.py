from src.data.scripts.create_db import create_db
from src.utils.generator import create_record

from src.utils import *

def main():
    create_record()          # si genera datos previos
    create_db()              # crea y limpia la base
    # insert_initial_data()    # inserta projects y devices

if __name__ == "__main__":
    main()
