
import pytest
from fastapi.testclient import TestClient

from backend.app.core.dependencies import get_repository
from backend.app.main import app
from backend.app.repositories.json_repository import JsonRepository


@pytest.fixture
def client(tmp_path):
    """Utiliza un repositorio JSON temporal para las pruebas."""
    repository = JsonRepository(tmp_path / "datos_prueba.json")
    repository.ensure_file()

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def crear_registro_eliminado(client, tipo):
    """Crea un registro y lo envía a la papelera."""

    configuracion = {
        "ingreso": {
            "ruta": "/api/ingresos",
            "datos": {
                "concepto": "Salario de prueba",
                "categoria": "salario",
                "monto": 2000000,
                "fecha": "2026-11-05",
            },
        },
        "gasto": {
            "ruta": "/api/gastos",
            "datos": {
                "concepto": "Mercado de prueba",
                "categoria": "alimentacion",
                "monto": 300000,
                "fecha": "2026-11-06",
            },
        },
        "presupuesto": {
            "ruta": "/api/presupuestos",
            "datos": {
                "mes": 11,
                "anio": 2026,
                "monto": 1000000,
            },
        },
    }

    elemento = configuracion[tipo]

    creacion = client.post(
        elemento["ruta"],
        json=elemento["datos"],
    )

    assert creacion.status_code == 201

    registro_id = creacion.json()["id"]

    eliminacion = client.delete(
        f"{elemento['ruta']}/{registro_id}"
    )

    assert eliminacion.status_code == 200

    return registro_id


def test_listar_papelera_consulta_todos_los_tipos(client):
    crear_registro_eliminado(client, "ingreso")
    crear_registro_eliminado(client, "gasto")
    crear_registro_eliminado(client, "presupuesto")

    respuesta = client.get("/api/papelera")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 3

    tipos = {registro["tipo"] for registro in respuesta.json()}

    assert tipos == {"ingreso", "gasto", "presupuesto"}


@pytest.mark.parametrize(
    "tipo",
    ["ingreso", "gasto", "presupuesto"],
)
def test_filtrar_papelera_por_tipo(client, tipo):
    crear_registro_eliminado(client, "ingreso")
    crear_registro_eliminado(client, "gasto")
    crear_registro_eliminado(client, "presupuesto")

    respuesta = client.get(
        "/api/papelera",
        params={"tipo": tipo},
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["tipo"] == tipo


def test_restaurar_ingreso(client):
    registro_id = crear_registro_eliminado(client, "ingreso")

    respuesta = client.post(
        f"/api/papelera/ingreso/{registro_id}/restaurar"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == registro_id

    papelera = client.get(
        "/api/papelera",
        params={"tipo": "ingreso"},
    )

    ingresos = client.get("/api/ingresos")

    assert papelera.json() == []
    assert any(
        ingreso["id"] == registro_id
        for ingreso in ingresos.json()
    )


def test_restaurar_gasto(client):
    registro_id = crear_registro_eliminado(client, "gasto")

    respuesta = client.post(
        f"/api/papelera/gasto/{registro_id}/restaurar"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == registro_id

    papelera = client.get(
        "/api/papelera",
        params={"tipo": "gasto"},
    )

    gastos = client.get("/api/gastos")

    assert papelera.json() == []
    assert any(
        gasto["id"] == registro_id
        for gasto in gastos.json()
    )


def test_restaurar_presupuesto_sin_conflicto(client):
    registro_id = crear_registro_eliminado(client, "presupuesto")

    respuesta = client.post(
        f"/api/papelera/presupuesto/{registro_id}/restaurar"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == registro_id

    papelera = client.get(
        "/api/papelera",
        params={"tipo": "presupuesto"},
    )

    presupuestos = client.get("/api/presupuestos")

    assert papelera.json() == []
    assert any(
        presupuesto["id"] == registro_id
        for presupuesto in presupuestos.json()
    )


def test_rechazar_restauracion_de_presupuesto_duplicado(client):
    registro_id = crear_registro_eliminado(
        client,
        "presupuesto",
    )

    # Crear otro presupuesto activo para el mismo periodo.
    nuevo_presupuesto = client.post(
        "/api/presupuestos",
        json={
            "mes": 11,
            "anio": 2026,
            "monto": 1500000,
        },
    )

    assert nuevo_presupuesto.status_code == 201

    respuesta = client.post(
        f"/api/papelera/presupuesto/{registro_id}/restaurar"
    )

    assert respuesta.status_code == 409

    # El presupuesto original debe permanecer en la papelera.
    papelera = client.get(
        "/api/papelera",
        params={"tipo": "presupuesto"},
    )

    assert len(papelera.json()) == 1
    assert papelera.json()[0]["id"] == registro_id


@pytest.mark.parametrize(
    "tipo",
    ["ingreso", "gasto", "presupuesto"],
)
def test_eliminar_permanentemente_registro(client, tipo):
    registro_id = crear_registro_eliminado(client, tipo)

    respuesta = client.delete(
        f"/api/papelera/{tipo}/{registro_id}"
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == registro_id

    papelera = client.get(
        "/api/papelera",
        params={"tipo": tipo},
    )

    assert papelera.status_code == 200
    assert papelera.json() == []


def test_restaurar_registro_inexistente_devuelve_404(client):
    respuesta = client.post(
        "/api/papelera/ingreso/999/restaurar"
    )

    assert respuesta.status_code == 404


def test_eliminar_registro_inexistente_devuelve_404(client):
    respuesta = client.delete(
        "/api/papelera/gasto/999"
    )

    assert respuesta.status_code == 404


def test_no_eliminar_permanentemente_registro_activo(client):
    creacion = client.post(
        "/api/ingresos",
        json={
            "concepto": "Ingreso activo",
            "categoria": "salario",
            "monto": 2000000,
            "fecha": "2026-11-05",
        },
    )

    registro_id = creacion.json()["id"]

    respuesta = client.delete(
        f"/api/papelera/ingreso/{registro_id}"
    )

    assert respuesta.status_code == 404

    ingresos = client.get("/api/ingresos")

    assert any(
        ingreso["id"] == registro_id
        for ingreso in ingresos.json()
    )


def test_papelera_rechaza_tipo_invalido_en_consulta(client):
    respuesta = client.get(
        "/api/papelera",
        params={"tipo": "historial"},
    )

    assert respuesta.status_code == 422


@pytest.mark.parametrize(
    "metodo",
    ["post", "delete"],
)
def test_papelera_rechaza_tipo_invalido_en_operaciones(client, metodo):
    if metodo == "post":
        respuesta = client.post(
            "/api/papelera/otro/1/restaurar"
        )
    else:
        respuesta = client.delete(
            "/api/papelera/otro/1"
        )

    assert respuesta.status_code == 422
