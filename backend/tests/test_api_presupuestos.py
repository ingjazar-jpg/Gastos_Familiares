
import pytest
from fastapi.testclient import TestClient

from backend.app.core.dependencies import get_repository
from backend.app.main import app
from backend.app.repositories.json_repository import JsonRepository


@pytest.fixture
def client(tmp_path):
    """Crea un cliente de pruebas con un repositorio JSON temporal."""
    repository = JsonRepository(tmp_path / "datos_prueba.json")
    repository.ensure_file()

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_crear_presupuesto(client):
    respuesta = client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )

    assert respuesta.status_code == 201

    datos = respuesta.json()
    assert datos["id"] == 1
    assert datos["mes"] == 11
    assert datos["anio"] == 2026
    assert datos["monto"] == 1500000
    assert datos["eliminado"] is False


def test_listar_presupuestos(client):
    client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )
    client.post(
        "/api/presupuestos",
        json={"mes": 12, "anio": 2026, "monto": 2000000},
    )

    respuesta = client.get("/api/presupuestos")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 2


def test_filtrar_presupuestos_por_periodo(client):
    client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )
    client.post(
        "/api/presupuestos",
        json={"mes": 12, "anio": 2026, "monto": 2000000},
    )

    respuesta = client.get(
        "/api/presupuestos",
        params={"mes": 11, "anio": 2026},
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["mes"] == 11


def test_rechazar_presupuesto_duplicado(client):
    datos = {"mes": 11, "anio": 2026, "monto": 1500000}

    primera_respuesta = client.post("/api/presupuestos", json=datos)
    segunda_respuesta = client.post("/api/presupuestos", json=datos)

    assert primera_respuesta.status_code == 201
    assert segunda_respuesta.status_code == 409


def test_actualizar_presupuesto(client):
    creacion = client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )
    presupuesto_id = creacion.json()["id"]

    respuesta = client.put(
        f"/api/presupuestos/{presupuesto_id}",
        json={"mes": 11, "anio": 2026, "monto": 1800000},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == presupuesto_id
    assert respuesta.json()["monto"] == 1800000


def test_rechazar_actualizacion_con_periodo_duplicado(client):
    client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )
    segundo = client.post(
        "/api/presupuestos",
        json={"mes": 12, "anio": 2026, "monto": 2000000},
    )

    segundo_id = segundo.json()["id"]

    respuesta = client.put(
        f"/api/presupuestos/{segundo_id}",
        json={"mes": 11, "anio": 2026, "monto": 2000000},
    )

    assert respuesta.status_code == 409


def test_eliminar_presupuesto_logicamente(client):
    creacion = client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )
    presupuesto_id = creacion.json()["id"]

    eliminacion = client.delete(
        f"/api/presupuestos/{presupuesto_id}"
    )

    consulta = client.get("/api/presupuestos")

    assert eliminacion.status_code == 200
    assert consulta.status_code == 200
    assert consulta.json() == []


def test_presupuesto_inexistente_devuelve_404(client):
    actualizacion = client.put(
        "/api/presupuestos/999",
        json={"mes": 11, "anio": 2026, "monto": 1500000},
    )

    eliminacion = client.delete("/api/presupuestos/999")

    assert actualizacion.status_code == 404
    assert eliminacion.status_code == 404


def test_rechazar_datos_invalidos(client):
    respuesta = client.post(
        "/api/presupuestos",
        json={"mes": 11, "anio": 2026, "monto": 0},
    )

    assert respuesta.status_code == 422
