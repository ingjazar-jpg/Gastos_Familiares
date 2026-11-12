
from pydantic import BaseModel

from backend.app.repositories.json_repository import JsonRepository


COLECCION = "presupuestos"


class PresupuestoDuplicadoError(Exception):
    """Se produce cuando ya existe un presupuesto activo en el periodo."""


def listar_presupuestos(
    repository: JsonRepository,
    mes: int | None = None,
    anio: int | None = None,
) -> list[dict]:
    """Lista los presupuestos activos, opcionalmente filtrados por periodo."""
    data = repository.read()

    presupuestos = [
        presupuesto
        for presupuesto in data[COLECCION]
        if not presupuesto["eliminado"]
    ]

    if mes is not None:
        presupuestos = [
            presupuesto
            for presupuesto in presupuestos
            if presupuesto["mes"] == mes
        ]

    if anio is not None:
        presupuestos = [
            presupuesto
            for presupuesto in presupuestos
            if presupuesto["anio"] == anio
        ]

    return presupuestos


def _existe_presupuesto_activo(
    data: dict,
    mes: int,
    anio: int,
    excluir_id: int | None = None,
) -> bool:
    """Comprueba si ya existe un presupuesto activo para el periodo."""
    return any(
        presupuesto["mes"] == mes
        and presupuesto["anio"] == anio
        and not presupuesto["eliminado"]
        and presupuesto["id"] != excluir_id
        for presupuesto in data[COLECCION]
    )


def crear_presupuesto(
    repository: JsonRepository,
    datos: BaseModel,
) -> dict:
    """Crea un presupuesto si el periodo no tiene otro activo."""
    nuevo_presupuesto = datos.model_dump(mode="json")
    data = repository.read()

    if _existe_presupuesto_activo(
        data,
        nuevo_presupuesto["mes"],
        nuevo_presupuesto["anio"],
    ):
        raise PresupuestoDuplicadoError(
            "Ya existe un presupuesto activo para ese periodo."
        )

    nuevo_id = repository.allocate_id(COLECCION)

    # Se vuelve a leer para trabajar con el contador actualizado.
    data = repository.read()

    nuevo_presupuesto["id"] = nuevo_id
    nuevo_presupuesto["eliminado"] = False

    data[COLECCION].append(nuevo_presupuesto)
    repository.write(data)

    return nuevo_presupuesto


def actualizar_presupuesto(
    repository: JsonRepository,
    presupuesto_id: int,
    datos: BaseModel,
) -> dict | None:
    """Actualiza un presupuesto activo conservando su identificador."""
    data = repository.read()

    indice = next(
        (
            indice
            for indice, presupuesto in enumerate(data[COLECCION])
            if presupuesto["id"] == presupuesto_id
            and not presupuesto["eliminado"]
        ),
        None,
    )

    if indice is None:
        return None

    actualizado = datos.model_dump(mode="json")

    if _existe_presupuesto_activo(
        data,
        actualizado["mes"],
        actualizado["anio"],
        excluir_id=presupuesto_id,
    ):
        raise PresupuestoDuplicadoError(
            "Ya existe otro presupuesto activo para ese periodo."
        )

    actualizado["id"] = presupuesto_id
    actualizado["eliminado"] = False

    data[COLECCION][indice] = actualizado
    repository.write(data)

    return actualizado


def eliminar_presupuesto(
    repository: JsonRepository,
    presupuesto_id: int,
) -> dict | None:
    """Marca un presupuesto como eliminado sin borrarlo del JSON."""
    data = repository.read()

    for presupuesto in data[COLECCION]:
        if (
            presupuesto["id"] == presupuesto_id
            and not presupuesto["eliminado"]
        ):
            presupuesto["eliminado"] = True
            repository.write(data)

            return {
                "mensaje": "Presupuesto eliminado correctamente.",
                "id": presupuesto_id,
            }

    return None
