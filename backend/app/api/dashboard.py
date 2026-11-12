
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.core.dependencies import get_repository
from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.dashboard import obtener_dashboard


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

RepositoryDependency = Annotated[
    JsonRepository,
    Depends(get_repository),
]


@router.get("")
def consultar_dashboard(
    repository: RepositoryDependency,
    mes: int = Query(..., ge=1, le=12),
    anio: int = Query(..., ge=1000, le=9999),
):
    """Obtiene el resumen financiero del periodo seleccionado."""

    return obtener_dashboard(
        repository=repository,
        mes=mes,
        anio=anio,
    )
