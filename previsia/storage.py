from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

DEFAULT_DATA_FILE = Path("data/temperatures.csv")


@dataclass(frozen=True)
class TemperatureRecord:
    day: date
    temperature: float


def _ensure_data_file(file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["day", "temperature"])


def list_temperature_records(file_path: Path = DEFAULT_DATA_FILE) -> list[TemperatureRecord]:
    _ensure_data_file(file_path)
    records: list[TemperatureRecord] = []

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records.append(
                TemperatureRecord(
                    day=date.fromisoformat(row["day"]),
                    temperature=float(row["temperature"]),
                )
            )

    return sorted(records, key=lambda item: item.day)


def _write_records(
    records: Iterable[TemperatureRecord], file_path: Path = DEFAULT_DATA_FILE
) -> None:
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["day", "temperature"])
        for item in sorted(records, key=lambda rec: rec.day):
            writer.writerow([item.day.isoformat(), f"{item.temperature:.2f}"])


def add_temperature_record(
    day: date, temperature: float, file_path: Path = DEFAULT_DATA_FILE
) -> None:
    records = list_temperature_records(file_path)
    filtered_records = [rec for rec in records if rec.day != day]
    filtered_records.append(TemperatureRecord(day=day, temperature=temperature))
    _write_records(filtered_records, file_path)
