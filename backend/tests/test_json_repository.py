
import json

import pytest

from backend.app.repositories.json_repository import JsonRepository


def test_creates_json_file_automatically(tmp_path):
    """El archivo debe crearse cuando todavía no existe."""
    file_path = tmp_path / "datos" / "datos_gastos.json"
    repository = JsonRepository(file_path)

    data = repository.read()

    assert file_path.exists()
    assert data["contadores"] == {
        "ingresos": 1,
        "gastos": 1,
        "presupuestos": 1,
    }
    assert data["ingresos"] == []
    assert data["gastos"] == []
    assert data["presupuestos"] == []


def test_persists_and_reads_data(tmp_path):
    """Los datos guardados deben poder recuperarse."""
    repository = JsonRepository(tmp_path / "datos_gastos.json")
    data = repository.initial_structure()

    data["ingresos"].append({
        "id": 1,
        "concepto": "Salario",
        "monto": 2500000,
    })

    repository.write(data)
    recovered_data = repository.read()

    assert recovered_data["ingresos"][0]["concepto"] == "Salario"
    assert recovered_data["ingresos"][0]["monto"] == 2500000


def test_allocates_sequential_ids(tmp_path):
    """Los IDs deben aumentar secuencialmente."""
    repository = JsonRepository(tmp_path / "datos_gastos.json")

    first_id = repository.allocate_id("ingresos")
    second_id = repository.allocate_id("ingresos")
    expense_id = repository.allocate_id("gastos")

    assert first_id == 1
    assert second_id == 2
    assert expense_id == 1


def test_ids_are_not_reused_after_record_removal(tmp_path):
    """Eliminar un registro no debe hacer retroceder el contador."""
    repository = JsonRepository(tmp_path / "datos_gastos.json")

    first_id = repository.allocate_id("ingresos")

    data = repository.read()
    data["ingresos"].append({"id": first_id})
    repository.write(data)

    data = repository.read()
    data["ingresos"].clear()
    repository.write(data)

    next_id = repository.allocate_id("ingresos")

    assert next_id == 2


def test_rejects_invalid_collection(tmp_path):
    """No debe permitir asignar IDs a colecciones desconocidas."""
    repository = JsonRepository(tmp_path / "datos_gastos.json")

    with pytest.raises(ValueError):
        repository.allocate_id("usuarios")


def test_rejects_invalid_json_without_overwriting(tmp_path):
    """Un JSON corrupto debe generar error sin ser sobrescrito."""
    file_path = tmp_path / "datos_gastos.json"
    invalid_content = '{"ingresos": '

    file_path.write_text(invalid_content, encoding="utf-8")
    repository = JsonRepository(file_path)

    with pytest.raises(RuntimeError, match="JSON inválido"):
        repository.read()

    assert file_path.read_text(encoding="utf-8") == invalid_content


def test_rejects_invalid_storage_structure(tmp_path):
    """No debe guardar estructuras incompletas."""
    repository = JsonRepository(tmp_path / "datos_gastos.json")

    with pytest.raises(ValueError):
        repository.write({"ingresos": []})
