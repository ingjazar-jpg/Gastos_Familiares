
import pytest

from backend.app.repositories.json_repository import JsonRepository
from backend.app.services.papelera import (
    eliminar_permanentemente,
    listar_papelera,
    restaurar_registro,
)
from backend.app.services.presupuestos import PresupuestoDuplicadoError


@pytest.fixture
def repository(tmp_path):
    """Crea un repositorio JSON temporal para cada prueba."""
    repo = JsonRepository(tmp_path / "datos_prueba.json")
    repo.ensure_file()
    return repo


def cargar_datos(repository, ingresos=None, gastos=None, presupuestos=None):
    """Carga datos de prueba en el repositorio."""
    repository.write({
        "contadores": {
            "ingresos": 10,
            "gastos": 10,
            "presupuestos": 10,
        },
        "ingresos": ingresos or [],
        "gastos": gastos or [],
        "presupuestos": presupuestos or [],
    })


def registro_ingreso(id=1, eliminado=True):
    return {
        "id": id,
        "concepto": "Salario",
        "categoria": "salario",
        "monto": 2000000,
        "fecha": "2026-11-05",
        "eliminado": eliminado,
    }


def registro_gasto(id=1, eliminado=True):
    return {
        "id": id,
        "concepto": "Mercado",
        "categoria": "alimentacion",
        "monto": 300000,
        "fecha": "2026-11-06",
        "eliminado": eliminado,
    }


def registro_presupuesto(id=1, eliminado=True):
    return {
        "id": id,
        "mes": 11,
        "anio": 2026,
        "monto": 1000000,
        "eliminado": eliminado,
    }


def test_listar_papelera_consulta_todos_los_tipos(repository):
    cargar_datos(
        repository,
        ingresos=[registro_ingreso()],
        gastos=[registro_gasto()],
        presupuestos=[registro_presupuesto()],
    )

    resultado = listar_papelera(repository)

    assert len(resultado) == 3
    assert {registro["tipo"] for registro in resultado} == {
        "ingreso",
        "gasto",
        "presupuesto",
    }


@pytest.mark.parametrize(
    ("tipo", "coleccion", "fabrica"),
    [
        ("ingreso", "ingresos", registro_ingreso),
        ("gasto", "gastos", registro_gasto),
        ("presupuesto", "presupuestos", registro_presupuesto),
    ],
)
def test_listar_papelera_filtra_por_tipo(
    repository,
    tipo,
    coleccion,
    fabrica,
):
    datos = {coleccion: [fabrica()]}
    cargar_datos(repository, **datos)

    resultado = listar_papelera(repository, tipo=tipo)

    assert len(resultado) == 1
    assert resultado[0]["tipo"] == tipo


def test_listar_papelera_rechaza_tipo_invalido(repository):
    with pytest.raises(ValueError):
        listar_papelera(repository, tipo="historial")


def test_restaurar_ingreso_conserva_identificador(repository):
    cargar_datos(
        repository,
        ingresos=[registro_ingreso(id=5)],
    )

    resultado = restaurar_registro(repository, "ingreso", 5)

    datos = repository.read()
    ingreso = datos["ingresos"][0]

    assert resultado == {
        "mensaje": "Registro restaurado correctamente.",
        "id": 5,
        "tipo": "ingreso",
    }
    assert ingreso["id"] == 5
    assert ingreso["eliminado"] is False


@pytest.mark.parametrize(
    "registro",
    [
        None,
        registro_ingreso(id=5, eliminado=False),
    ],
)
def test_no_restaurar_registro_inexistente_o_activo(repository, registro):
    cargar_datos(
        repository,
        ingresos=[] if registro is None else [registro],
    )

    resultado = restaurar_registro(repository, "ingreso", 5)

    assert resultado is None


def test_restaurar_presupuesto_sin_conflicto(repository):
    cargar_datos(
        repository,
        presupuestos=[registro_presupuesto(id=3)],
    )

    resultado = restaurar_registro(repository, "presupuesto", 3)

    datos = repository.read()

    assert resultado["id"] == 3
    assert resultado["tipo"] == "presupuesto"
    assert datos["presupuestos"][0]["eliminado"] is False


def test_rechazar_restauracion_de_presupuesto_duplicado(repository):
    presupuesto_eliminado = registro_presupuesto(id=1)
    presupuesto_activo = registro_presupuesto(id=2, eliminado=False)

    cargar_datos(
        repository,
        presupuestos=[
            presupuesto_eliminado,
            presupuesto_activo,
        ],
    )

    with pytest.raises(PresupuestoDuplicadoError):
        restaurar_registro(repository, "presupuesto", 1)

    datos = repository.read()

    # El presupuesto eliminado debe permanecer en la papelera.
    assert datos["presupuestos"][0]["eliminado"] is True


def test_eliminar_permanentemente_registro_de_papelera(repository):
    cargar_datos(
        repository,
        ingresos=[registro_ingreso(id=5)],
    )

    resultado = eliminar_permanentemente(repository, "ingreso", 5)

    datos = repository.read()

    assert resultado == {
        "mensaje": "Registro eliminado permanentemente.",
        "id": 5,
        "tipo": "ingreso",
    }
    assert datos["ingresos"] == []

    # La eliminación física no debe modificar el contador.
    assert datos["contadores"]["ingresos"] == 10


def test_no_eliminar_permanentemente_registro_activo(repository):
    cargar_datos(
        repository,
        gastos=[registro_gasto(id=4, eliminado=False)],
    )

    resultado = eliminar_permanentemente(repository, "gasto", 4)

    datos = repository.read()

    assert resultado is None
    assert len(datos["gastos"]) == 1
    assert datos["gastos"][0]["eliminado"] is False


def test_eliminar_permanentemente_registro_inexistente(repository):
    cargar_datos(repository)

    resultado = eliminar_permanentemente(
        repository,
        "ingreso",
        999,
    )

    assert resultado is None


@pytest.mark.parametrize(
    "operacion",
    [
        "restaurar",
        "eliminar",
    ],
)
def test_operaciones_rechazan_tipo_invalido(repository, operacion):
    cargar_datos(repository)

    with pytest.raises(ValueError):
        if operacion == "restaurar":
            restaurar_registro(repository, "otro", 1)
        else:
            eliminar_permanentemente(repository, "otro", 1)
