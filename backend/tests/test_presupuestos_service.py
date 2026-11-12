
import pytest

from backend.app.repositories.json_repository import JsonRepository
from backend.app.schemas.presupuesto import PresupuestoCreate
from backend.app.services.presupuestos import (
    PresupuestoDuplicadoError,
    actualizar_presupuesto,
    crear_presupuesto,
    eliminar_presupuesto,
    listar_presupuestos,
)


@pytest.fixture
def repository(tmp_path):
    """Repositorio aislado para las pruebas de presupuestos."""
    return JsonRepository(tmp_path / "presupuestos_prueba.json")


def datos_presupuesto(mes=11, anio=2026, monto=1500000):
    return PresupuestoCreate(
        mes=mes,
        anio=anio,
        monto=monto,
    )


def test_crear_presupuesto_asigna_id_y_estado_activo(repository):
    resultado = crear_presupuesto(repository, datos_presupuesto())

    assert resultado["id"] == 1
    assert resultado["mes"] == 11
    assert resultado["anio"] == 2026
    assert resultado["monto"] == 1500000
    assert resultado["eliminado"] is False


def test_no_permite_dos_presupuestos_activos_en_el_mismo_periodo(repository):
    crear_presupuesto(repository, datos_presupuesto())

    with pytest.raises(PresupuestoDuplicadoError):
        crear_presupuesto(repository, datos_presupuesto(monto=2000000))


def test_permite_presupuestos_en_periodos_diferentes(repository):
    primero = crear_presupuesto(repository, datos_presupuesto())
    segundo = crear_presupuesto(
        repository,
        datos_presupuesto(mes=12, anio=2026),
    )

    assert primero["id"] == 1
    assert segundo["id"] == 2


def test_listar_presupuestos_filtra_por_periodo(repository):
    crear_presupuesto(repository, datos_presupuesto())
    crear_presupuesto(
        repository,
        datos_presupuesto(mes=12, anio=2026),
    )

    resultado = listar_presupuestos(repository, mes=11, anio=2026)

    assert len(resultado) == 1
    assert resultado[0]["mes"] == 11


def test_actualizar_presupuesto_conserva_id(repository):
    creado = crear_presupuesto(repository, datos_presupuesto())

    actualizado = actualizar_presupuesto(
        repository,
        creado["id"],
        datos_presupuesto(mes=12, anio=2026, monto=1800000),
    )

    assert actualizado is not None
    assert actualizado["id"] == creado["id"]
    assert actualizado["mes"] == 12
    assert actualizado["monto"] == 1800000


def test_no_permite_actualizar_a_un_periodo_duplicado(repository):
    primero = crear_presupuesto(repository, datos_presupuesto())
    segundo = crear_presupuesto(
        repository,
        datos_presupuesto(mes=12, anio=2026),
    )

    with pytest.raises(PresupuestoDuplicadoError):
        actualizar_presupuesto(
            repository,
            segundo["id"],
            datos_presupuesto(mes=11, anio=2026),
        )

    # El presupuesto original no debe modificarse.
    activos = listar_presupuestos(repository)
    assert len(activos) == 2
    assert activos[0]["id"] == primero["id"]


def test_eliminar_presupuesto_es_logico(repository):
    creado = crear_presupuesto(repository, datos_presupuesto())

    resultado = eliminar_presupuesto(repository, creado["id"])

    assert resultado["id"] == creado["id"]
    assert listar_presupuestos(repository) == []

    data = repository.read()
    assert data["presupuestos"][0]["eliminado"] is True


def test_permite_crear_otro_presupuesto_en_periodo_eliminado(repository):
    primero = crear_presupuesto(repository, datos_presupuesto())
    eliminar_presupuesto(repository, primero["id"])

    segundo = crear_presupuesto(
        repository,
        datos_presupuesto(monto=2000000),
    )

    assert segundo["id"] == 2
    assert segundo["monto"] == 2000000


def test_presupuesto_inexistente_no_se_actualiza_ni_elimina(repository):
    actualizado = actualizar_presupuesto(
        repository,
        999,
        datos_presupuesto(),
    )
    eliminado = eliminar_presupuesto(repository, 999)

    assert actualizado is None
    assert eliminado is None
