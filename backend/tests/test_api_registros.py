
import pytest
from fastapi.testclient import TestClient

from backend.app.core.dependencies import get_repository
from backend.app.main import app
from backend.app.repositories.json_repository import JsonRepository


@pytest.fixture
def client(tmp_path):
    """Cliente de pruebas con un repositorio JSON temporal."""
    repository = JsonRepository(tmp_path / "datos_prueba.json")

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "endpoint,payload,payload_actualizado,categoria",
    [
        (
            "/api/ingresos",
            {
                "concepto": "Salario mensual",
                "categoria": "salario",
                "monto": 2500000,
                "fecha": "2026-11-09",
            },
            {
                "concepto": "Salario actualizado",
                "categoria": "salario",
                "monto": 2700000,
                "fecha": "2026-11-10",
            },
            "salario",
        ),
        (
            "/api/gastos",
            {
                "concepto": "Compra de alimentos",
                "categoria": "alimentacion",
                "monto": 150000,
                "fecha": "2026-11-09",
            },
            {
                "concepto": "Compra de alimentos actualizada",
                "categoria": "alimentacion",
                "monto": 180000,
                "fecha": "2026-11-10",
            },
            "alimentacion",
        ),
    ],
)
def test_ciclo_completo_de_registro(
    client, endpoint, payload, payload_actualizado, categoria
):
    # 1. Crear registro.
    respuesta = client.post(endpoint, json=payload)

    assert respuesta.status_code == 201
    registro_creado = respuesta.json()
    registro_id = registro_creado["id"]

    assert registro_creado["concepto"] == payload["concepto"]
    assert registro_creado["eliminado"] is False

    # 2. Consultar y filtrar registros.
    respuesta = client.get(
        endpoint,
        params={
            "mes": 11,
            "anio": 2026,
            "categoria": categoria,
        },
    )

    assert respuesta.status_code == 200
    registros = respuesta.json()
    assert len(registros) == 1
    assert registros[0]["id"] == registro_id

    # 3. Actualizar registro.
    respuesta = client.put(
        f"{endpoint}/{registro_id}",
        json=payload_actualizado,
    )

    assert respuesta.status_code == 200
    registro_actualizado = respuesta.json()

    assert registro_actualizado["id"] == registro_id
    assert registro_actualizado["concepto"] == payload_actualizado["concepto"]
    assert registro_actualizado["monto"] == payload_actualizado["monto"]

    # 4. Eliminar lógicamente.
    respuesta = client.delete(f"{endpoint}/{registro_id}")

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == registro_id

    # 5. Confirmar que ya no aparece en la consulta activa.
    respuesta = client.get(endpoint)

    assert respuesta.status_code == 200
    assert respuesta.json() == []


@pytest.mark.parametrize(
    "endpoint",
    ["/api/ingresos", "/api/gastos"],
)
def test_rechaza_datos_invalidos(client, endpoint):
    payload = {
        "concepto": "Registro inválido",
        "categoria": "otros",
        "monto": 0,
        "fecha": "2026-11-09",
    }

    respuesta = client.post(endpoint, json=payload)

    assert respuesta.status_code == 422


@pytest.mark.parametrize(
    "endpoint",
    ["/api/ingresos", "/api/gastos"],
)
def test_registro_inexistente_devuelve_404(client, endpoint):
    payload = {
        "concepto": "Registro de prueba",
        "categoria": "otros",
        "monto": 10000,
        "fecha": "2026-11-09",
    }

    respuesta_edicion = client.put(
        f"{endpoint}/999",
        json=payload,
    )
    respuesta_eliminacion = client.delete(f"{endpoint}/999")

    assert respuesta_edicion.status_code == 404
    assert respuesta_eliminacion.status_code == 404
