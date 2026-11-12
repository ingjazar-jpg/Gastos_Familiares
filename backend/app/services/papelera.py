
from typing import Any

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.presupuestos import PresupuestoDuplicadoError


TIPOS_COLECCIONES = {
    "ingreso": "ingresos",
    "gasto": "gastos",
    "presupuesto": "presupuestos",
}


def _obtener_coleccion(tipo: str) -> str:
    """Valida el tipo y devuelve el nombre de su colección."""
    if tipo not in TIPOS_COLECCIONES:
        raise ValueError(f"Tipo de registro no válido: {tipo}.")

    return TIPOS_COLECCIONES[tipo]


def listar_papelera(
    repository: JsonRepository,
    tipo: str | None = None,
) -> list[dict[str, Any]]:
    """Lista los registros eliminados, opcionalmente por tipo."""

    if tipo is not None:
        colecciones = {tipo: _obtener_coleccion(tipo)}
    else:
        colecciones = TIPOS_COLECCIONES

    data = repository.read()
    registros_eliminados = []

    for tipo_registro, coleccion in colecciones.items():
        for registro in data[coleccion]:
            if registro["eliminado"]:
                registros_eliminados.append({
                    **registro,
                    "tipo": tipo_registro,
                })

    return registros_eliminados


def restaurar_registro(
    repository: JsonRepository,
    tipo: str,
    registro_id: int,
) -> dict[str, Any] | None:
    """
    Restaura un registro eliminado conservando su identificador.

    Impide restaurar un presupuesto cuando ya existe otro
    presupuesto activo para el mismo mes y año.
    """

    coleccion = _obtener_coleccion(tipo)
    data = repository.read()

    registro = next(
        (
            elemento
            for elemento in data[coleccion]
            if elemento["id"] == registro_id
            and elemento["eliminado"]
        ),
        None,
    )

    if registro is None:
        return None

    if tipo == "presupuesto":
        existe_otro_activo = any(
            presupuesto["mes"] == registro["mes"]
            and presupuesto["anio"] == registro["anio"]
            and not presupuesto["eliminado"]
            and presupuesto["id"] != registro_id
            for presupuesto in data["presupuestos"]
        )

        if existe_otro_activo:
            raise PresupuestoDuplicadoError(
                "No se puede restaurar el presupuesto porque "
                "ya existe otro presupuesto activo para ese periodo."
            )

    registro["eliminado"] = False
    repository.write(data)

    return {
        "mensaje": "Registro restaurado correctamente.",
        "id": registro_id,
        "tipo": tipo,
    }


def eliminar_permanentemente(
    repository: JsonRepository,
    tipo: str,
    registro_id: int,
) -> dict[str, Any] | None:
    """
    Elimina físicamente un registro de la papelera.

    Solo permite eliminar registros que ya estén marcados
    como eliminados. Los contadores de identificadores
    permanecen intactos.
    """

    coleccion = _obtener_coleccion(tipo)
    data = repository.read()

    indice = next(
        (
            indice
            for indice, registro in enumerate(data[coleccion])
            if registro["id"] == registro_id
            and registro["eliminado"]
        ),
        None,
    )

    if indice is None:
        return None

    data[coleccion].pop(indice)
    repository.write(data)

    return {
        "mensaje": "Registro eliminado permanentemente.",
        "id": registro_id,
        "tipo": tipo,
    }
