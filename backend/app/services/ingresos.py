
from typing import Any

from pydantic import BaseModel

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.registro_service import (
    actualizar_registro,
    crear_registro,
    eliminar_registro,
    listar_registros,
)


COLECCION = "ingresos"


def listar_ingresos(
    repository: JsonRepository,
    mes: int | None = None,
    anio: int | None = None,
    categoria: str | None = None,
) -> list[dict[str, Any]]:
    return listar_registros(repository, COLECCION, mes, anio, categoria)


def crear_ingreso(
    repository: JsonRepository,
    datos: BaseModel,
) -> dict[str, Any]:
    return crear_registro(repository, COLECCION, datos)


def actualizar_ingreso(
    repository: JsonRepository,
    ingreso_id: int,
    datos: BaseModel,
) -> dict[str, Any] | None:
    return actualizar_registro(repository, COLECCION, ingreso_id, datos)


def eliminar_ingreso(
    repository: JsonRepository,
    ingreso_id: int,
) -> dict[str, Any] | None:
    return eliminar_registro(repository, COLECCION, ingreso_id)
