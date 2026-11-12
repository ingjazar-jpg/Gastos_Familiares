
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.app.core.dependencies import get_repository
from backend.app.repositories.json_repository import JsonRepository
from backend.app.schemas.presupuesto import PresupuestoCreate
from backend.app.services.presupuestos import (
    PresupuestoDuplicadoError,
    actualizar_presupuesto,
    crear_presupuesto,
    eliminar_presupuesto,
    listar_presupuestos,
)


router = APIRouter(
    prefix="/api/presupuestos",
    tags=["Presupuestos"],
)

RepositoryDependency = Annotated[
    JsonRepository,
    Depends(get_repository),
]


@router.get("")
def obtener_presupuestos(
    repository: RepositoryDependency,
    mes: int | None = Query(default=None, ge=1, le=12),
    anio: int | None = Query(default=None, ge=1000, le=9999),
):
    return listar_presupuestos(repository, mes, anio)


@router.post("", status_code=status.HTTP_201_CREATED)
def registrar_presupuesto(
    datos: PresupuestoCreate,
    repository: RepositoryDependency,
):
    try:
        return crear_presupuesto(repository, datos)
    except PresupuestoDuplicadoError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put("/{presupuesto_id}")
def modificar_presupuesto(
    presupuesto_id: int,
    datos: PresupuestoCreate,
    repository: RepositoryDependency,
):
    try:
        resultado = actualizar_presupuesto(
            repository,
            presupuesto_id,
            datos,
        )
    except PresupuestoDuplicadoError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El presupuesto solicitado no existe o está eliminado.",
        )

    return resultado


@router.delete("/{presupuesto_id}")
def borrar_presupuesto(
    presupuesto_id: int,
    repository: RepositoryDependency,
):
    resultado = eliminar_presupuesto(repository, presupuesto_id)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El presupuesto solicitado no existe o ya está eliminado.",
        )

    return resultado
