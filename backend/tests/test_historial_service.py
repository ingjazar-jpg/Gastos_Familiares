
import pytest

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.historial import listar_historial


@pytest.fixture
def repository(tmp_path):
    """Crea un repositorio JSON temporal para cada prueba."""
    repo = JsonRepository(tmp_path / "datos_prueba.json")
    repo.ensure_file()
    return repo


def cargar_datos(repository, ingresos=None, gastos=None):
    """Carga registros de prueba en el repositorio."""
    repository.write({
        "contadores": {
            "ingresos": 1,
            "gastos": 1,
            "presupuestos": 1,
        },
        "ingresos": ingresos or [],
        "gastos": gastos or [],
        "presupuestos": [],
    })


def test_historial_unifica_y_ordena_registros(repository):
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
                "fecha": "2026-11-06",
                "eliminado": False,
            },
        ],
    )

    resultado = listar_historial(repository)

    assert len(resultado) == 3
    assert resultado[0]["concepto"] == "Transporte"
    assert resultado[1]["concepto"] == "Mercado"
    assert resultado[2]["concepto"] == "Salario"

    assert resultado[0]["tipo"] == "gasto"
    assert resultado[2]["tipo"] == "ingreso"


def test_historial_filtra_por_periodo(repository):
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

    resultado = listar_historial(
        repository,
        mes=11,
        anio=2026,
    )

    assert len(resultado) == 1
    assert resultado[0]["concepto"] == "Ingreso noviembre"


def test_historial_filtra_por_tipo(repository):
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
                "monto": 300000,
                "fecha": "2026-11-06",
                "eliminado": False,
            },
        ],
    )

    resultado = listar_historial(repository, tipo="gasto")

    assert len(resultado) == 1
    assert resultado[0]["tipo"] == "gasto"
    assert resultado[0]["concepto"] == "Mercado"


def test_historial_filtra_por_categoria(repository):
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
                "concepto": "Transporte",
                "categoria": "transporte",
                "monto": 100000,
                "fecha": "2026-11-06",
                "eliminado": False,
            },
        ],
    )

    resultado = listar_historial(
        repository,
        categoria="alimentacion",
    )

    assert len(resultado) == 1
    assert resultado[0]["categoria"] == "alimentacion"
    assert resultado[0]["concepto"] == "Mercado"


def test_historial_excluye_registros_eliminados(repository):
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
    )

    resultado = listar_historial(repository)

    assert len(resultado) == 1
    assert resultado[0]["concepto"] == "Ingreso activo"


@pytest.mark.parametrize(
    "parametros",
    [
        {"mes": 11},
        {"anio": 2026},
    ],
)
def test_historial_exige_mes_y_anio_juntos(repository, parametros):
    with pytest.raises(ValueError):
        listar_historial(repository, **parametros)


def test_historial_rechaza_tipo_no_valido(repository):
    with pytest.raises(ValueError):
        listar_historial(repository, tipo="presupuesto")


def test_historial_sin_registros_devuelve_lista_vacia(repository):
    resultado = listar_historial(repository)

    assert resultado == []


def test_historial_ordena_por_id_descendente_en_misma_fecha(repository):
    cargar_datos(
        repository,
        gastos=[
            {
                "id": 1,
                "concepto": "Gasto uno",
                "categoria": "alimentacion",
                "monto": 100000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
            {
                "id": 2,
                "concepto": "Gasto dos",
                "categoria": "transporte",
                "monto": 200000,
                "fecha": "2026-11-05",
                "eliminado": False,
            },
        ],
    )

    resultado = listar_historial(repository, tipo="gasto")

    assert [registro["id"] for registro in resultado] == [2, 1]
