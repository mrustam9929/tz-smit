import decimal
import json
from typing import List, Optional

from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.param_functions import Depends

from tz_smit.db.dao.tariff_dao import TariffDAO, get_tariff_dao
from tz_smit.web.api.tariff.schema import (
    CalculateTariffRequest,
    CalculateTariffResponse,
    TariffCreate,
    TariffResponse,
    TariffUpload,
)

router = APIRouter()


@router.post("/upload/")
async def create_tariffs(
    tariffs_data: TariffUpload,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
):
    tariffs = []
    for tariff_date, items in tariffs_data.data.items():
        for item in items:
            tariffs.append(
                {
                    "date": tariff_date,
                    "rate": item.rate,
                    "cargo_type": item.cargo_type,
                },
            )
    await tariff_dao.bulk_create(tariffs)
    return {"message": "Tariffs successfully created"}


@router.post("/upload-file/")
async def upload_tariffs(
    file: UploadFile,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
):
    """
    API для загрузки тарифов из JSON-файла.
    """
    try:
        content = await file.read()
        data = json.loads(content)
        validated_data = TariffUpload(data=data)
        tariffs = []
        for tariff_date, items in validated_data.data.items():
            for item in items:
                tariffs.append(
                    {
                        "date": tariff_date,
                        "rate": item.rate,
                        "cargo_type": item.cargo_type,
                    },
                )
        await tariff_dao.bulk_create(tariffs)
        return {"message": "Tariffs successfully created"}
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON file",
        )


@router.post("/calculate/")
async def calculate_tariffs(
    request: CalculateTariffRequest,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
) -> CalculateTariffResponse:
    tariffs = await tariff_dao.filter_by_fields(
        fields={"date": request.date, "cargo_type": request.cargo_type},
    )
    if not tariffs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid tariff params",
        )
    amount = tariffs[0].rate * request.amount
    return CalculateTariffResponse(amount=amount)


@router.post("/tariffs/", response_model=TariffResponse)
async def create_tariff(
    tariff: TariffCreate,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
):
    created_tariff = await tariff_dao.create(
        cargo_type=tariff.cargo_type,
        rate=tariff.rate,
        date=tariff.date,
    )
    return created_tariff


@router.get("/tariffs/{tariff_id}/", response_model=TariffResponse)
async def get_tariff(tariff_id: int, tariff_dao: TariffDAO = Depends(get_tariff_dao)):
    tariff = await tariff_dao.get(tariff_id)
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return tariff


@router.get("/tariffs/", response_model=List[TariffResponse])
async def get_tariffs(
    limit: int = 10,
    offset: int = 0,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
):
    return await tariff_dao.get_all(limit=limit, offset=offset)


@router.put("/tariffs/{tariff_id}/", response_model=TariffResponse)
async def update_tariff(
    tariff_id: int,
    cargo_type: Optional[str] = None,
    rate: Optional[decimal.Decimal] = None,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
):
    updated_tariff = await tariff_dao.update(
        tariff_id,
        cargo_type=cargo_type,
        rate=rate,
    )
    if not updated_tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return updated_tariff


@router.delete("/tariffs/{tariff_id}/", response_model=dict)
async def delete_tariff(
    tariff_id: int,
    tariff_dao: TariffDAO = Depends(get_tariff_dao),
):
    success = await tariff_dao.delete(tariff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return {"message": "Tariff successfully deleted"}
