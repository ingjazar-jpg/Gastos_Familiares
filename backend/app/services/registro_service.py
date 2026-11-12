
from typing import Any

from pydantic import BaseModel

from backend.app.repositories.json_repository import JsonRepository


def listar_registros(
    repository: JsonRepository,
    collection: str,
    mes: int | None = None,
    anio: int | None = None,
    categoria: str | None = None,
) -> list[dict[str, Any]]:
    """Consulta registros activos con filtros opcionales."""

    if collection not in repository.COLLECTIONS:
        raise ValueError(f"Colección no válida: {collection}.")

    data = repository.read()
    registros = [
        registro
        for registro in data[collection]
        if not registro["eliminado"]
    ]

    if mes is not None:
        registros = [
            registro
            for registro in registros
            if int(registro["fecha"][5:7]) == mes
        ]

    if anio is not None:
        registros = [
            registro
            for registro in registros
            if int(registro["fecha"][0:4]) == anio
        ]

    if categoria is not None:
        valor_categoria = getattr(categoria, "value", categoria)
        registros = [
            registro
            for registro in registros
            if registro["categoria"] == valor_categoria
        ]

    return registros


def crear_registro(
    repository: JsonRepository,
    collection: str,
    datos: BaseModel,
) -> dict[str, Any]:
    """Crea un registro y asigna su identificador secuencial."""

    if collection not in repository.COLLECTIONS:
        raise ValueError(f"Colección no válida: {collection}.")

    nuevo_id = repository.allocate_id(collection)

    registro = datos.model_dump(mode="json")
    registro["id"] = nuevo_id
    registro["eliminado"] = False

    data = repository.read()
    data[collection].append(registro)
    repository.write(data)

    return registro


def actualizar_registro(
    repository: JsonRepository,
    collection: str,
    registro_id: int,
    datos: BaseModel,
) -> dict[str, Any] | None:
    """Reemplaza los campos editables de un registro activo."""

    if collection not in repository.COLLECTIONS:
        raise ValueError(f"Colección no válida: {collection}.")

    data = repository.read()

    for indice, registro in enumerate(data[collection]):
        if registro["id"] == registro_id and not registro["eliminado"]:
            actualizado = datos.model_dump(mode="json")
            actualizado["id"] = registro_id
            actualizado["eliminado"] = False

            data[collection][indice] = actualizado
            repository.write(data)

            return actualizado

    return None


def eliminar_registro(
    repository: JsonRepository,
    collection: str,
    registro_id: int,
) -> dict[str, Any] | None:
    """Marca un registro activo como eliminado, sin borrarlo del JSON."""

    if collection not in repository.COLLECTIONS:
        raise ValueError(f"Colección no válida: {collection}.")

    data = repository.read()

    for registro in data[collection]:
        if registro["id"] == registro_id and not registro["eliminado"]:
            registro["eliminado"] = True
            repository.write(data)

            return {
                "mensaje": "Registro eliminado correctamente.",
                "id": registro_id,
            }

    return None