import logging
import uuid

from fastapi import Depends, Path, Request
from fastapi.responses import JSONResponse

from app.router import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health")


@router.get("")
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
