
import pytest

from backend.app.repositories.json_repository import JsonRepository
from backend.app.schemas.gasto import GastoCreate
from backend.app.schemas.ingreso import IngresoCreate
from backend.app.services.gastos import (
    actualizar_gasto,
    crear_gasto,
    eliminar_gasto,
    listar_gastos,
)
from backend.app.services.ingresos import (
    actualizar_ingreso,
    crear_ingreso,
    eliminar_ingreso,
    listar_ingresos,
)


@pytest.fixture
def repository(tmp_path):
    repo = JsonRepository(tmp_path / "datos_gastos.json")
    repo.ensure_file()
    return repo


def test_crear_ingreso_asigna_id_y_estado_activo(repository):
    datos = IngresoCreate(
        concepto="Salario mensual",
        categoria="salario",
        monto=2500000,
        fecha="2026-11-01",
    )

    resultado = crear_ingreso(repository, datos)

    assert resultado["id"] == 1
    assert resultado["eliminado"] is False
    assert resultado["monto"] == 2500000


def test_listar_ingresos_filtra_por_periodo_y_categoria(repository):
    crear_ingreso(
        repository,
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=2500000,
            fecha="2026-11-01",
        ),
    )
    crear_ingreso(
        repository,
        IngresoCreate(
            concepto="Honorarios",
            categoria="honorarios",
            monto=500000,
            fecha="2026-10-15",
        ),
    )

    resultado = listar_ingresos(
        repository,
        mes=11,
        anio=2026,
        categoria="salario",
    )

    assert len(resultado) == 1
    assert resultado[0]["concepto"] == "Salario"


def test_actualizar_ingreso_conserva_id(repository):
    ingreso = crear_ingreso(
        repository,
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=2000000,
            fecha="2026-11-01",
        ),
    )

    datos_actualizados = IngresoCreate(
        concepto="Salario actualizado",
        categoria="salario",
        monto=2800000,
        fecha="2026-11-02",
    )

    resultado = actualizar_ingreso(
        repository,
        ingreso["id"],
        datos_actualizados,
    )

    assert resultado is not None
    assert resultado["id"] == ingreso["id"]
    assert resultado["concepto"] == "Salario actualizado"
    assert resultado["monto"] == 2800000


def test_eliminar_ingreso_es_logico(repository):
    ingreso = crear_ingreso(
        repository,
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=2000000,
            fecha="2026-11-01",
        ),
    )

    resultado = eliminar_ingreso(repository, ingreso["id"])

    assert resultado is not None
    assert listar_ingresos(repository) == []

    data = repository.read()
    assert data["ingresos"][0]["eliminado"] is True


def test_crear_gasto_asigna_id_y_estado_activo(repository):
    datos = GastoCreate(
        concepto="Mercado",
        categoria="alimentacion",
        monto=180000,
        fecha="2026-11-03",
    )

    resultado = crear_gasto(repository, datos)

    assert resultado["id"] == 1
    assert resultado["eliminado"] is False
    assert resultado["categoria"] == "alimentacion"


def test_listar_gastos_filtra_por_periodo(repository):
    crear_gasto(
        repository,
        GastoCreate(
            concepto="Mercado",
            categoria="alimentacion",
            monto=180000,
            fecha="2026-11-03",
        ),
    )
    crear_gasto(
        repository,
        GastoCreate(
            concepto="Transporte",
            categoria="transporte",
            monto=50000,
            fecha="2026-10-10",
        ),
    )

    resultado = listar_gastos(repository, mes=11, anio=2026)

    assert len(resultado) == 1
    assert resultado[0]["concepto"] == "Mercado"


def test_actualizar_gasto_conserva_id(repository):
    gasto = crear_gasto(
        repository,
        GastoCreate(
            concepto="Mercado",
            categoria="alimentacion",
            monto=180000,
            fecha="2026-11-03",
        ),
    )

    datos_actualizados = GastoCreate(
        concepto="Mercado semanal",
        categoria="alimentacion",
        monto=200000,
        fecha="2026-11-04",
    )

    resultado = actualizar_gasto(
        repository,
        gasto["id"],
        datos_actualizados,
    )

    assert resultado is not None
    assert resultado["id"] == gasto["id"]
    assert resultado["concepto"] == "Mercado semanal"
    assert resultado["monto"] == 200000


def test_eliminar_gasto_es_logico(repository):
    gasto = crear_gasto(
        repository,
        GastoCreate(
            concepto="Mercado",
            categoria="alimentacion",
            monto=180000,
            fecha="2026-11-03",
        ),
    )

    resultado = eliminar_gasto(repository, gasto["id"])

    assert resultado is not None
    assert listar_gastos(repository) == []

    data = repository.read()
    assert data["gastos"][0]["eliminado"] is True


def test_registro_inexistente_no_se_actualiza_ni_elimina(repository):
    datos_ingreso = IngresoCreate(
        concepto="Salario",
        categoria="salario",
        monto=2000000,
        fecha="2026-11-01",
    )

    assert actualizar_ingreso(repository, 999, datos_ingreso) is None
    assert eliminar_ingreso(repository, 999) is None

    datos_gasto = GastoCreate(
        concepto="Mercado",
        categoria="alimentacion",
        monto=180000,
        fecha="2026-11-03",
    )

    assert actualizar_gasto(repository, 999, datos_gasto) is None
    assert eliminar_gasto(repository, 999) is None


def test_identificadores_no_se_reutilizan(repository):
    primero = crear_ingreso(
        repository,
        IngresoCreate(
            concepto="Primer ingreso",
            categoria="salario",
            monto=1000000,
            fecha="2026-11-01",
        ),
    )

    eliminar_ingreso(repository, primero["id"])

    segundo = crear_ingreso(
        repository,
        IngresoCreate(
            concepto="Segundo ingreso",
            categoria="honorarios",
            monto=500000,
            fecha="2026-11-02",
        ),
    )

    assert primero["id"] == 1
    assert segundo["id"] == 2
