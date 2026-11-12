
from typing import Any

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.presupuestos import listar_presupuestos
from backend.app.services.registro_service import listar_registros


def obtener_dashboard(
    repository: JsonRepository,
    mes: int,
    anio: int,
) -> dict[str, Any]:
    """
    Consolida los datos financieros de un periodo para el Dashboard.

    Excluye automáticamente los registros eliminados mediante los
    servicios de consulta existentes.
    """

    # Obtener ingresos y gastos activos del periodo.
    ingresos = listar_registros(
        repository,
        "ingresos",
        mes=mes,
        anio=anio,
    )

    gastos = listar_registros(
        repository,
        "gastos",
        mes=mes,
        anio=anio,
    )

    # Calcular totales financieros.
    total_ingresos = sum(registro["monto"] for registro in ingresos)
    total_gastos = sum(registro["monto"] for registro in gastos)

    balance = total_ingresos - total_gastos

    # Consultar el presupuesto activo del periodo.
    presupuestos = listar_presupuestos(
        repository,
        mes=mes,
        anio=anio,
    )

    presupuesto = presupuestos[0] if presupuestos else None

    if presupuesto is None:
        presupuesto_monto = None
        presupuesto_disponible = None
        porcentaje_ejecucion = None
        estado_presupuesto = "sin_presupuesto"

    else:
        presupuesto_monto = presupuesto["monto"]

        presupuesto_disponible = presupuesto_monto - total_gastos

        porcentaje_ejecucion = round(
            total_gastos * 100 / presupuesto_monto,
            2,
        )

        # Las comparaciones con enteros evitan problemas de precisión
        # al evaluar los límites del 80 % y del 100 %.
        if total_gastos > presupuesto_monto:
            estado_presupuesto = "excedido"

        elif total_gastos * 100 >= presupuesto_monto * 80:
            estado_presupuesto = "advertencia"

        else:
            estado_presupuesto = "normal"

    # Agrupar los gastos por categoría para el gráfico.
    gastos_por_categoria: dict[str, int] = {}

    for gasto in gastos:
        categoria = gasto["categoria"]

        gastos_por_categoria[categoria] = (
            gastos_por_categoria.get(categoria, 0)
            + gasto["monto"]
        )

    datos_gastos_categoria = [
        {
            "categoria": categoria,
            "total": total,
        }
        for categoria, total in sorted(gastos_por_categoria.items())
    ]

    return {
        "periodo": {
            "mes": mes,
            "anio": anio,
        },
        "resumen": {
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "balance": balance,
        },
        "presupuesto": {
            "configurado": presupuesto is not None,
            "monto": presupuesto_monto,
            "disponible": presupuesto_disponible,
            "porcentaje_ejecucion": porcentaje_ejecucion,
            "estado": estado_presupuesto,
        },
        "graficos": {
            "gastos_por_categoria": datos_gastos_categoria,
            "ingresos_vs_gastos": [
                {
                    "tipo": "ingresos",
                    "total": total_ingresos,
                },
                {
                    "tipo": "gastos",
                    "total": total_gastos,
                },
            ],
        },
    }
