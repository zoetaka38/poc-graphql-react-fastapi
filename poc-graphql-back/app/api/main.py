from fastapi import APIRouter

from .health.views import router as health_router

router = APIRouter()

router.include_router(health_router)
