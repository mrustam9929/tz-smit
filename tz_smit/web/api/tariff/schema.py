import datetime
import decimal
from typing import Dict, List

from pydantic import BaseModel, validator


class TariffItem(BaseModel):
    cargo_type: str
    rate: decimal.Decimal

    @validator("rate")
    def validate_rate(cls, value):
        if value <= 0:
            raise ValueError("Rate must be greater than 0")
        return value


class TariffUpload(BaseModel):
    data: Dict[datetime.date, List[TariffItem]]

    @validator("data", pre=True)
    def validate_and_convert_keys(cls, value):
        if not isinstance(value, dict):
            raise ValueError("data must be a dictionary")
        corrected_data = {}
        for key, items in value.items():
            try:
                # Преобразование строкового ключа в `datetime.date`
                key_date = datetime.datetime.strptime(key, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"Invalid date format for key: {key}. Use 'YYYY-MM-DD'.",
                )
            corrected_data[key_date] = items
        return corrected_data


class CalculateTariffRequest(BaseModel):
    amount: decimal.Decimal
    date: datetime.date
    cargo_type: str


class CalculateTariffResponse(BaseModel):
    amount: decimal.Decimal


class TariffCreate(BaseModel):
    cargo_type: str
    rate: decimal.Decimal
    date: datetime.datetime


class TariffResponse(BaseModel):
    id: int
    cargo_type: str
    rate: decimal.Decimal
    date: datetime.datetime

    class Config:
        orm_mode = True
