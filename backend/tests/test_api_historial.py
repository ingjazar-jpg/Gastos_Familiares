
import pytest
from fastapi.testclient import TestClient

from backend.app.core.dependencies import get_repository
from backend.app.main import app
from backend.app.repositories.json_repository import JsonRepository


@pytest.fixture
def client(tmp_path):
    """Prepara un repositorio temporal para las pruebas de API."""
    repository = JsonRepository(tmp_path / "datos_prueba.json")
    repository.ensure_file()

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_historial_unifica_y_ordena_registros(client):
    # Crear un ingreso.
    ingreso = client.post(
        "/api/ingresos",
        json={
            "concepto": "Salario",
            "categoria": "salario",
            "monto": 3000000,
            "fecha": "2026-11-05",
        },
    )

    # Crear dos gastos con la misma fecha.
    gasto_mercado = client.post(
        "/api/gastos",
        json={
            "concepto": "Mercado",
            "categoria": "alimentacion",
            "monto": 400000,
            "fecha": "2026-11-06",
        },
    )

    gasto_transporte = client.post(
        "/api/gastos",
        json={
            "concepto": "Transporte",
            "categoria": "transporte",
            "monto": 200000,
            "fecha": "2026-11-06",
        },
    )

    assert ingreso.status_code == 201
    assert gasto_mercado.status_code == 201
    assert gasto_transporte.status_code == 201

    respuesta = client.get("/api/historial")

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert len(datos) == 3
    assert [registro["concepto"] for registro in datos] == [
        "Transporte",
        "Mercado",
        "Salario",
    ]

    assert datos[0]["tipo"] == "gasto"
    assert datos[2]["tipo"] == "ingreso"


def test_historial_filtra_por_periodo(client):
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
        "/api/historial",
        params={"mes": 11, "anio": 2026},
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["concepto"] == "Ingreso noviembre"


def test_historial_filtra_por_tipo(client):
    client.post(
        "/api/ingresos",
        json={
            "concepto": "Salario",
            "categoria": "salario",
            "monto": 2000000,
            "fecha": "2026-11-05",
        },
    )

    client.post(
        "/api/gastos",
        json={
            "concepto": "Mercado",
            "categoria": "alimentacion",
            "monto": 300000,
            "fecha": "2026-11-06",
        },
    )

    respuesta = client.get(
        "/api/historial",
        params={"tipo": "gasto"},
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["tipo"] == "gasto"


def test_historial_filtra_por_categoria(client):
    client.post(
        "/api/gastos",
        json={
            "concepto": "Mercado",
            "categoria": "alimentacion",
            "monto": 300000,
            "fecha": "2026-11-05",
        },
    )

    client.post(
        "/api/gastos",
        json={
            "concepto": "Transporte",
            "categoria": "transporte",
            "monto": 100000,
            "fecha": "2026-11-06",
        },
    )

    respuesta = client.get(
        "/api/historial",
        params={"categoria": "alimentacion"},
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["categoria"] == "alimentacion"


def test_historial_excluye_registros_eliminados(client):
    ingreso_activo = client.post(
        "/api/ingresos",
        json={
            "concepto": "Ingreso activo",
            "categoria": "salario",
            "monto": 2000000,
            "fecha": "2026-11-05",
        },
    )

    ingreso_eliminado = client.post(
        "/api/ingresos",
        json={
            "concepto": "Ingreso eliminado",
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

    respuesta = client.get("/api/historial")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["concepto"] == "Ingreso activo"


@pytest.mark.parametrize(
    "parametros",
    [
        {"mes": 11},
        {"anio": 2026},
    ],
)
def test_historial_exige_mes_y_anio_juntos(client, parametros):
    respuesta = client.get(
        "/api/historial",
        params=parametros,
    )

    assert respuesta.status_code == 422


def test_historial_rechaza_tipo_no_valido(client):
    respuesta = client.get(
        "/api/historial",
        params={"tipo": "presupuesto"},
    )

    assert respuesta.status_code == 422


def test_historial_sin_registros_devuelve_lista_vacia(client):
    respuesta = client.get("/api/historial")

    assert respuesta.status_code == 200
    assert respuesta.json() == []


@pytest.mark.parametrize(
    "parametros",
    [
        {"mes": 0, "anio": 2026},
        {"mes": 13, "anio": 2026},
        {"mes": 11, "anio": 999},
    ],
)
def test_historial_rechaza_parametros_fuera_de_rango(
    client,
    parametros,
):
    respuesta = client.get(
        "/api/historial",
        params=parametros,
    )

    assert respuesta.status_code == 422
