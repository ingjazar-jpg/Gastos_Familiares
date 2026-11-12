import pytest
from pydantic import ValidationError

from backend.app.schemas.ingreso import IngresoCreate, IngresoResponse
from backend.app.schemas.gasto import GastoCreate
from backend.app.schemas.presupuesto import PresupuestoCreate


def test_ingreso_valido():
    ingreso = IngresoCreate(
        concepto=" Salario mensual ",
        categoria="salario",
        monto=2500000,
        fecha="2026-11-01",
    )

    assert ingreso.concepto == "Salario mensual"
    assert ingreso.monto == 2500000
    assert ingreso.fecha.isoformat() == "2026-11-01"


def test_ingreso_rechaza_monto_cero():
    with pytest.raises(ValidationError):
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=0,
            fecha="2026-11-01",
        )


def test_ingreso_rechaza_monto_decimal():
    with pytest.raises(ValidationError):
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=2500000.50,
            fecha="2026-11-01",
        )


def test_ingreso_rechaza_categoria_no_permitida():
    with pytest.raises(ValidationError):
        IngresoCreate(
            concepto="Salario",
            categoria="arriendo",
            monto=2500000,
            fecha="2026-11-01",
        )


def test_ingreso_rechaza_concepto_vacio():
    with pytest.raises(ValidationError):
        IngresoCreate(
            concepto="   ",
            categoria="salario",
            monto=2500000,
            fecha="2026-11-01",
        )


def test_ingreso_rechaza_fecha_invalida():
    with pytest.raises(ValidationError):
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=2500000,
            fecha="2026-15-40",
        )


def test_gasto_valido():
    gasto = GastoCreate(
        concepto="Mercado semanal",
        categoria="alimentacion",
        monto=180000,
        fecha="2026-11-03",
    )

    assert gasto.categoria.value == "alimentacion"
    assert gasto.monto == 180000


def test_gasto_rechaza_categoria_no_permitida():
    with pytest.raises(ValidationError):
        GastoCreate(
            concepto="Mercado",
            categoria="salario",
            monto=180000,
            fecha="2026-11-03",
        )


def test_presupuesto_valido():
    presupuesto = PresupuestoCreate(
        mes=11,
        anio=2026,
        monto=3000000,
    )

    assert presupuesto.mes == 11
    assert presupuesto.anio == 2026
    assert presupuesto.monto == 3000000


@pytest.mark.parametrize("mes", [0, 13])
def test_presupuesto_rechaza_mes_fuera_de_rango(mes):
    with pytest.raises(ValidationError):
        PresupuestoCreate(
            mes=mes,
            anio=2026,
            monto=3000000,
        )


def test_presupuesto_rechaza_anio_no_valido():
    with pytest.raises(ValidationError):
        PresupuestoCreate(
            mes=11,
            anio=99,
            monto=3000000,
        )


def test_presupuesto_rechaza_monto_decimal():
    with pytest.raises(ValidationError):
        PresupuestoCreate(
            mes=11,
            anio=2026,
            monto=3000000.50,
        )


def test_esquema_respuesta_ingreso():
    ingreso = IngresoResponse(
        id=1,
        concepto="Salario mensual",
        categoria="salario",
        monto=2500000,
        fecha="2026-11-01",
        eliminado=False,
    )

    assert ingreso.id == 1
    assert ingreso.eliminado is False
    assert ingreso.model_dump(mode="json")["categoria"] == "salario"


def test_esquema_entrada_rechaza_campos_no_definidos():
    with pytest.raises(ValidationError):
        IngresoCreate(
            concepto="Salario",
            categoria="salario",
            monto=2500000,
            fecha="2026-11-01",
            id=99,
        )