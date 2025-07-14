from .generator import create_record
from .load_records import main as insert_initial_data

__all__ = [
    "create_record",
    "insert_initial_data"
]