
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.app.core.dependencies import get_repository
from backend.app.repositories.json_repository import JsonRepository
from backend.app.schemas.gasto import GastoCreate
from backend.app.services.gastos import (
    actualizar_gasto,
    crear_gasto,
    eliminar_gasto,
    listar_gastos,
)


router = APIRouter(prefix="/api/gastos", tags=["Gastos"])

RepositoryDependency = Annotated[
    JsonRepository,
    Depends(get_repository),
]


@router.get("")
def obtener_gastos(
    repository: RepositoryDependency,
    mes: int | None = Query(default=None, ge=1, le=12),
    anio: int | None = Query(default=None, ge=1000, le=9999),
    categoria: str | None = None,
):
    return listar_gastos(repository, mes, anio, categoria)


@router.post("", status_code=status.HTTP_201_CREATED)
def registrar_gasto(
    datos: GastoCreate,
    repository: RepositoryDependency,
):
    return crear_gasto(repository, datos)


@router.put("/{gasto_id}")
def modificar_gasto(
    gasto_id: int,
    datos: GastoCreate,
    repository: RepositoryDependency,
):
    resultado = actualizar_gasto(repository, gasto_id, datos)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El gasto solicitado no existe o está eliminado.",
        )

    return resultado


@router.delete("/{gasto_id}")
def borrar_gasto(
    gasto_id: int,
    repository: RepositoryDependency,
):
    resultado = eliminar_gasto(repository, gasto_id)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El gasto solicitado no existe o ya está eliminado.",
        )

    return resultado
