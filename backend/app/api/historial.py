
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.core.dependencies import get_repository
from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.historial import listar_historial


router = APIRouter(
    prefix="/api/historial",
    tags=["Historial"],
)

RepositoryDependency = Annotated[
    JsonRepository,
    Depends(get_repository),
]


@router.get("")
def consultar_historial(
    repository: RepositoryDependency,
    mes: int | None = Query(default=None, ge=1, le=12),
    anio: int | None = Query(default=None, ge=1000, le=9999),
    tipo: Literal["ingreso", "gasto"] | None = Query(default=None),
    categoria: str | None = Query(default=None),
):
    """Consulta el historial unificado de ingresos y gastos."""

    if (mes is None) != (anio is None):
        raise HTTPException(
            status_code=422,
            detail="Los parámetros mes y anio deben proporcionarse juntos.",
        )

    try:
        return listar_historial(
            repository=repository,
            mes=mes,
            anio=anio,
            tipo=tipo,
            categoria=categoria,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error
