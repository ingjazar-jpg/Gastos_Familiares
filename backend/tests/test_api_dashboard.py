
import pytest
from fastapi.testclient import TestClient

from backend.app.core.dependencies import get_repository
from backend.app.main import app
from backend.app.repositories.json_repository import JsonRepository


@pytest.fixture
def client(tmp_path):
    """Utiliza un repositorio temporal para las pruebas de API."""
    repository = JsonRepository(tmp_path / "datos_prueba.json")
    repository.ensure_file()

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_consultar_dashboard_con_datos_completos(client):
    # Registrar un ingreso.
    ingreso = client.post(
        "/api/ingresos",
        json={
            "concepto": "Salario",
            "categoria": "salario",
            "monto": 3000000,
            "fecha": "2026-11-05",
        },
    )
    assert ingreso.status_code == 201

    # Registrar dos gastos.
    gasto_alimentacion = client.post(
        "/api/gastos",
        json={
            "concepto": "Mercado",
            "categoria": "alimentacion",
            "monto": 400000,
            "fecha": "2026-11-06",
        },
    )
    assert gasto_alimentacion.status_code == 201

    gasto_transporte = client.post(
        "/api/gastos",
        json={
            "concepto": "Transporte",
            "categoria": "transporte",
            "monto": 200000,
            "fecha": "2026-11-07",
        },
    )
    assert gasto_transporte.status_code == 201

    # Configurar el presupuesto del periodo.
    presupuesto = client.post(
        "/api/presupuestos",
        json={
            "mes": 11,
            "anio": 2026,
            "monto": 1000000,
        },
    )
    assert presupuesto.status_code == 201

    # Consultar el Dashboard.
    respuesta = client.get(
        "/api/dashboard",
        params={"mes": 11, "anio": 2026},
    )

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert datos["periodo"] == {
        "mes": 11,
        "anio": 2026,
    }

    assert datos["resumen"] == {
        "total_ingresos": 3000000,
        "total_gastos": 600000,
        "balance": 2400000,
    }

    assert datos["presupuesto"] == {
        "configurado": True,
        "monto": 1000000,
        "disponible": 400000,
        "porcentaje_ejecucion": 60,
        "estado": "normal",
    }

    assert datos["graficos"]["gastos_por_categoria"] == [
        {"categoria": "alimentacion", "total": 400000},
        {"categoria": "transporte", "total": 200000},
    ]

    assert datos["graficos"]["ingresos_vs_gastos"] == [
        {"tipo": "ingresos", "total": 3000000},
        {"tipo": "gastos", "total": 600000},
    ]


def test_dashboard_sin_presupuesto(client):
    client.post(
        "/api/gastos",
        json={
            "concepto": "Mercado",
            "categoria": "alimentacion",
            "monto": 300000,
            "fecha": "2026-11-05",
        },
    )

    respuesta = client.get(
        "/api/dashboard",
        params={"mes": 11, "anio": 2026},
    )

    assert respuesta.status_code == 200

    presupuesto = respuesta.json()["presupuesto"]

    assert presupuesto["configurado"] is False
    assert presupuesto["monto"] is None
    assert presupuesto["disponible"] is None
    assert presupuesto["porcentaje_ejecucion"] is None
    assert presupuesto["estado"] == "sin_presupuesto"


def test_dashboard_excluye_registros_eliminados(client):
    ingreso_activo = client.post(
        "/api/ingresos",
        json={
            "concepto": "Salario",
            "categoria": "salario",
            "monto": 2000000,
            "fecha": "2026-11-05",
        },
    )

    ingreso_eliminado = client.post(
        "/api/ingresos",
        json={
            "concepto": "Venta",
            "categoria": "ventas",
            "monto": 500000,
            "fecha": "2026-11-06",
        },
    )

    assert ingreso_activo.status_code == 201
    assert ingreso_eliminado.status_code == 201

    ingreso_id = ingreso_eliminado.json()["id"]

    eliminacion = client.delete(
        f"/api/ingresos/{ingreso_id}"
    )
    assert eliminacion.status_code == 200

    respuesta = client.get(
        "/api/dashboard",
        params={"mes": 11, "anio": 2026},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["resumen"]["total_ingresos"] == 2000000


def test_dashboard_filtra_por_periodo(client):
    client.post(
        "/api/ingresos",
        json={
            "concepto": "Ingreso noviembre",
            "categoria": "salario",
            "monto": 2000000,
            "fecha": "2026-11-05",
        },
    )

    client.post(
        "/api/ingresos",
        json={
            "concepto": "Ingreso octubre",
            "categoria": "honorarios",
            "monto": 1000000,
            "fecha": "2026-10-05",
        },
    )

    respuesta = client.get(
        "/api/dashboard",
        params={"mes": 11, "anio": 2026},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["resumen"]["total_ingresos"] == 2000000


@pytest.mark.parametrize(
    "parametros",
    [
        {"anio": 2026},
        {"mes": 11},
        {"mes": 0, "anio": 2026},
        {"mes": 13, "anio": 2026},
        {"mes": 11, "anio": 999},
    ],
)
def test_dashboard_rechaza_parametros_invalidos(client, parametros):
    respuesta = client.get(
        "/api/dashboard",
        params=parametros,
    )

    assert respuesta.status_code == 422
