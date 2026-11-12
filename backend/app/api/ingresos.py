
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.app.core.dependencies import get_repository
from backend.app.repositories.json_repository import JsonRepository
from backend.app.schemas.ingreso import IngresoCreate
from backend.app.services.ingresos import (
    actualizar_ingreso,
    crear_ingreso,
    eliminar_ingreso,
    listar_ingresos,
)


router = APIRouter(prefix="/api/ingresos", tags=["Ingresos"])

RepositoryDependency = Annotated[
    JsonRepository,
    Depends(get_repository),
]


@router.get("")
def obtener_ingresos(
    repository: RepositoryDependency,
    mes: int | None = Query(default=None, ge=1, le=12),
    anio: int | None = Query(default=None, ge=1000, le=9999),
    categoria: str | None = None,
):
    return listar_ingresos(repository, mes, anio, categoria)


@router.post("", status_code=status.HTTP_201_CREATED)
def registrar_ingreso(
    datos: IngresoCreate,
    repository: RepositoryDependency,
):
    return crear_ingreso(repository, datos)


@router.put("/{ingreso_id}")
def modificar_ingreso(
    ingreso_id: int,
    datos: IngresoCreate,
    repository: RepositoryDependency,
):
    resultado = actualizar_ingreso(repository, ingreso_id, datos)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ingreso solicitado no existe o está eliminado.",
        )

    return resultado


@router.delete("/{ingreso_id}")
def borrar_ingreso(
    ingreso_id: int,
    repository: RepositoryDependency,
):
    resultado = eliminar_ingreso(repository, ingreso_id)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ingreso solicitado no existe o ya está eliminado.",
        )

    return resultado
