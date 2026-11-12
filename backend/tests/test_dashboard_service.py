
import pytest

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.dashboard import obtener_dashboard


@pytest.fixture
def repository(tmp_path):
    """Prepara un repositorio JSON independiente para cada prueba."""
    repo = JsonRepository(tmp_path / "datos_prueba.json")
    repo.ensure_file()
    return repo


def cargar_datos(repository, ingresos=None, gastos=None, presupuestos=None):
    """Carga datos de prueba en el repositorio."""
    repository.write({
        "contadores": {
            "ingresos": 1,
            "gastos": 1,
            "presupuestos": 1,
        },
        "ingresos": ingresos or [],
        "gastos": gastos or [],
        "presupuestos": presupuestos or [],
    })


def test_dashboard_sin_registros_ni_presupuesto(repository):
    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["periodo"] == {"mes": 11, "anio": 2026}
    assert resultado["resumen"]["total_ingresos"] == 0
    assert resultado["resumen"]["total_gastos"] == 0
    assert resultado["resumen"]["balance"] == 0

    assert resultado["presupuesto"]["configurado"] is False
    assert resultado["presupuesto"]["monto"] is None
    assert resultado["presupuesto"]["disponible"] is None
    assert resultado["presupuesto"]["porcentaje_ejecucion"] is None
    assert resultado["presupuesto"]["estado"] == "sin_presupuesto"


def test_dashboard_calcula_resumen_financiero(repository):
    cargar_datos(
        repository,
        ingresos=[
            {
                "id": 1,
                "concepto": "Salario",
                "categoria": "salario",
                "monto": 3000000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
        ],
        gastos=[
            {
                "id": 1,
                "concepto": "Mercado",
                "categoria": "alimentacion",
                "monto": 400000,
                "fecha": "2026-11-06",
                "eliminado": False,
            },
            {
                "id": 2,
                "concepto": "Transporte",
                "categoria": "transporte",
                "monto": 200000,
                "fecha": "2026-11-07",
                "eliminado": False,
            },
        ],
        presupuestos=[
            {
                "id": 1,
                "mes": 11,
                "anio": 2026,
                "monto": 1000000,
                "eliminado": False,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["resumen"] == {
        "total_ingresos": 3000000,
        "total_gastos": 600000,
        "balance": 2400000,
    }

    assert resultado["presupuesto"]["monto"] == 1000000
    assert resultado["presupuesto"]["disponible"] == 400000
    assert resultado["presupuesto"]["porcentaje_ejecucion"] == 60
    assert resultado["presupuesto"]["estado"] == "normal"


def test_dashboard_excluye_registros_eliminados(repository):
    cargar_datos(
        repository,
        ingresos=[
            {
                "id": 1,
                "concepto": "Ingreso activo",
                "categoria": "salario",
                "monto": 2000000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
            {
                "id": 2,
                "concepto": "Ingreso eliminado",
                "categoria": "ventas",
                "monto": 500000,
                "fecha": "2026-11-06",
                "eliminado": True,
            },
        ],
        gastos=[
            {
                "id": 1,
                "concepto": "Gasto activo",
                "categoria": "alimentacion",
                "monto": 300000,
                "fecha": "2026-11-07",
                "eliminado": False,
            },
            {
                "id": 2,
                "concepto": "Gasto eliminado",
                "categoria": "transporte",
                "monto": 100000,
                "fecha": "2026-11-08",
                "eliminado": True,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["resumen"]["total_ingresos"] == 2000000
    assert resultado["resumen"]["total_gastos"] == 300000


def test_dashboard_excluye_registros_de_otros_periodos(repository):
    cargar_datos(
        repository,
        ingresos=[
            {
                "id": 1,
                "concepto": "Ingreso noviembre",
                "categoria": "salario",
                "monto": 2000000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
            {
                "id": 2,
                "concepto": "Ingreso octubre",
                "categoria": "honorarios",
                "monto": 1000000,
                "fecha": "2026-10-05",
                "eliminado": False,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["resumen"]["total_ingresos"] == 2000000


def test_dashboard_calcula_gastos_por_categoria(repository):
    cargar_datos(
        repository,
        gastos=[
            {
                "id": 1,
                "concepto": "Mercado",
                "categoria": "alimentacion",
                "monto": 300000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
            {
                "id": 2,
                "concepto": "Restaurante",
                "categoria": "alimentacion",
                "monto": 100000,
                "fecha": "2026-11-06",
                "eliminado": False,
            },
            {
                "id": 3,
                "concepto": "Transporte",
                "categoria": "transporte",
                "monto": 200000,
                "fecha": "2026-11-07",
                "eliminado": False,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["graficos"]["gastos_por_categoria"] == [
        {"categoria": "alimentacion", "total": 400000},
        {"categoria": "transporte", "total": 200000},
    ]


@pytest.mark.parametrize(
    ("total_gastos", "estado"),
    [
        (79000, "normal"),
        (80000, "advertencia"),
        (100000, "advertencia"),
        (100001, "excedido"),
    ],
)
def test_dashboard_aplica_limites_de_alerta(
    repository,
    total_gastos,
    estado,
):
    cargar_datos(
        repository,
        gastos=[
            {
                "id": 1,
                "concepto": "Gasto de prueba",
                "categoria": "alimentacion",
                "monto": total_gastos,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
        ],
        presupuestos=[
            {
                "id": 1,
                "mes": 11,
                "anio": 2026,
                "monto": 100000,
                "eliminado": False,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["presupuesto"]["estado"] == estado


def test_dashboard_muestra_disponible_negativo_al_exceder_presupuesto(
    repository,
):
    cargar_datos(
        repository,
        gastos=[
            {
                "id": 1,
                "concepto": "Gasto",
                "categoria": "vivienda",
                "monto": 120000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
        ],
        presupuestos=[
            {
                "id": 1,
                "mes": 11,
                "anio": 2026,
                "monto": 100000,
                "eliminado": False,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["presupuesto"]["disponible"] == -20000
    assert resultado["presupuesto"]["porcentaje_ejecucion"] == 120
    assert resultado["presupuesto"]["estado"] == "excedido"


def test_dashboard_genera_datos_para_comparar_ingresos_y_gastos(repository):
    cargar_datos(
        repository,
        ingresos=[
            {
                "id": 1,
                "concepto": "Salario",
                "categoria": "salario",
                "monto": 2000000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
        ],
        gastos=[
            {
                "id": 1,
                "concepto": "Mercado",
                "categoria": "alimentacion",
                "monto": 500000,
                "fecha": "2026-11-06",
                "eliminado": False,
            },
        ],
    )

    resultado = obtener_dashboard(repository, mes=11, anio=2026)

    assert resultado["graficos"]["ingresos_vs_gastos"] == [
        {"tipo": "ingresos", "total": 2000000},
        {"tipo": "gastos", "total": 500000},
    ]
