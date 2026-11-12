
from typing import Any

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.registro_service import listar_registros


TIPOS_VALIDOS = {
    "ingreso": "ingresos",
    "gasto": "gastos",
}


def listar_historial(
    repository: JsonRepository,
    mes: int | None = None,
    anio: int | None = None,
    tipo: str | None = None,
    categoria: str | None = None,
) -> list[dict[str, Any]]:
    """
    Consulta el historial unificado de ingresos y gastos activos.

    Permite filtrar por periodo, tipo y categoría. Ordena los
    resultados por fecha descendente y, en caso de empate,
    por identificador descendente.
    """

    # El filtro de periodo requiere mes y año conjuntamente.
    if (mes is None) != (anio is None):
        raise ValueError(
            "Los parámetros mes y anio deben proporcionarse juntos."
        )

    # Validar el tipo de registro solicitado.
    if tipo is not None and tipo not in TIPOS_VALIDOS:
        raise ValueError(
            "El tipo debe ser 'ingreso' o 'gasto'."
        )

    # Determinar las colecciones que se consultarán.
    tipos_consulta = (
        {tipo: TIPOS_VALIDOS[tipo]}
        if tipo is not None
        else TIPOS_VALIDOS
    )

    historial = []

    for tipo_registro, coleccion in tipos_consulta.items():
        registros = listar_registros(
            repository=repository,
            collection=coleccion,
            mes=mes,
            anio=anio,
            categoria=categoria,
        )

        for registro in registros:
            historial.append({
                **registro,
                "tipo": tipo_registro,
            })

    # Ordenar por fecha descendente e ID descendente.
    historial.sort(
        key=lambda registro: (
            registro["fecha"],
            registro["id"],
        ),
        reverse=True,
    )

    return historial
