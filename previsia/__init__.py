"""Pacote principal do PrevisIA."""

from .recommender import generate_recommendation
from .storage import add_temperature_record, list_temperature_records

__all__ = [
    "generate_recommendation",
    "add_temperature_record",
    "list_temperature_records",
]
