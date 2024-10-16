import logging
from functools import partial

from fastapi.routing import APIRouter as _APIRouter

logger = logging.getLogger(__name__)


APIRouter = partial(_APIRouter)
