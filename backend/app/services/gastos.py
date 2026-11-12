
from typing import Any

from pydantic import BaseModel

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.registro_service import (
    actualizar_registro,
    crear_registro,
    eliminar_registro,
    listar_registros,
)


COLECCION = "gastos"


def listar_gastos(
    repository: JsonRepository,
    mes: int | None = None,
    anio: int | None = None,
    categoria: str | None = None,
) -> list[dict[str, Any]]:
    return listar_registros(repository, COLECCION, mes, anio, categoria)


def crear_gasto(
    repository: JsonRepository,
    datos: BaseModel,
) -> dict[str, Any]:
    return crear_registro(repository, COLECCION, datos)


def actualizar_gasto(
    repository: JsonRepository,
    gasto_id: int,
    datos: BaseModel,
) -> dict[str, Any] | None:
    return actualizar_registro(repository, COLECCION, gasto_id, datos)


def eliminar_gasto(
    repository: JsonRepository,
    gasto_id: int,
) -> dict[str, Any] | None:
    return eliminar_registro(repository, COLECCION, gasto_id)
