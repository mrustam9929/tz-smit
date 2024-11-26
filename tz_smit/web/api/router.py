from fastapi.routing import APIRouter

from tz_smit.web.api import echo, kafka, tariff

api_router = APIRouter()
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(tariff.router, prefix="/tariffs", tags=["tariffs"])
api_router.include_router(kafka.router, prefix="/kafka", tags=["kafka"])
