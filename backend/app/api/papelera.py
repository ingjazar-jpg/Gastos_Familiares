
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.app.core.dependencies import get_repository
from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.papelera import (
    eliminar_permanentemente,
    listar_papelera,
    restaurar_registro,
)
from backend.app.services.presupuestos import PresupuestoDuplicadoError


router = APIRouter(
    prefix="/api/papelera",
    tags=["Papelera"],
)

RepositoryDependency = Annotated[
    JsonRepository,
    Depends(get_repository),
]


@router.get("")
def consultar_papelera(
    repository: RepositoryDependency,
    tipo: str | None = Query(default=None),
):
    """Consulta los registros eliminados de la aplicación."""

    try:
        return listar_papelera(
            repository=repository,
            tipo=tipo,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error


@router.post("/{tipo}/{registro_id}/restaurar")
def restaurar_elemento_papelera(
    tipo: str,
    registro_id: int,
    repository: RepositoryDependency,
):
    """Restaura un registro eliminado."""

    try:
        resultado = restaurar_registro(
            repository=repository,
            tipo=tipo,
            registro_id=registro_id,
        )
    except PresupuestoDuplicadoError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el registro eliminado.",
        )

    return resultado


@router.delete("/{tipo}/{registro_id}")
def eliminar_elemento_papelera(
    tipo: str,
    registro_id: int,
    repository: RepositoryDependency,
):
    """Elimina permanentemente un registro de la papelera."""

    try:
        resultado = eliminar_permanentemente(
            repository=repository,
            tipo=tipo,
            registro_id=registro_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el registro eliminado en la papelera.",
        )

    return resultado
