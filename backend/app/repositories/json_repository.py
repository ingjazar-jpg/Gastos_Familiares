
import json
from pathlib import Path
from typing import Any

from backend.app.core.config import DATA_FILE


class JsonRepository:
    """Gestiona la lectura y escritura del almacenamiento JSON."""

    COLLECTIONS = ("ingresos", "gastos", "presupuestos")

    def __init__(self, file_path: Path | None = None):
        self.file_path = Path(file_path or DATA_FILE)

    @staticmethod
    def initial_structure() -> dict[str, Any]:
        """Estructura inicial del almacenamiento."""
        return {
            "contadores": {
                "ingresos": 1,
                "gastos": 1,
                "presupuestos": 1,
            },
            "ingresos": [],
            "gastos": [],
            "presupuestos": [],
        }

    def _validate_structure(self, data: Any) -> None:
        """Comprueba la estructura general antes de guardar."""
        if not isinstance(data, dict):
            raise ValueError("La raíz del archivo JSON debe ser un objeto.")

        required_keys = {"contadores", *self.COLLECTIONS}

        if not required_keys.issubset(data):
            raise ValueError("La estructura del archivo JSON está incompleta.")

        counters = data["contadores"]

        if not isinstance(counters, dict):
            raise ValueError("Los contadores deben ser un objeto.")

        for collection in self.COLLECTIONS:
            if collection not in counters:
                raise ValueError(f"Falta el contador de {collection}.")

            if (
                not isinstance(counters[collection], int)
                or isinstance(counters[collection], bool)
                or counters[collection] < 1
            ):
                raise ValueError(
                    f"El contador de {collection} debe ser un entero positivo."
                )

            if not isinstance(data[collection], list):
                raise ValueError(
                    f"La colección {collection} debe ser una lista."
                )

    def ensure_file(self) -> None:
        """Crea el directorio y archivo si todavía no existen."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.write(self.initial_structure())

    def read(self) -> dict[str, Any]:
        """Lee y devuelve los datos almacenados."""
        self.ensure_file()

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "El archivo de datos contiene JSON inválido. "
                "Se conserva el archivo para evitar pérdida de información."
            ) from error

        self._validate_structure(data)
        return data

    def write(self, data: dict[str, Any]) -> None:
        """Guarda los datos directamente en el archivo JSON."""
        self._validate_structure(data)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def allocate_id(self, collection: str) -> int:
        """
        Reserva el siguiente ID de una colección.

        El contador se incrementa y persiste antes de devolver el ID.
        Nunca se reutilizan identificadores.
        """
        if collection not in self.COLLECTIONS:
            raise ValueError(f"Colección no válida: {collection}.")

        data = self.read()

        new_id = data["contadores"][collection]
        data["contadores"][collection] = new_id + 1

        self.write(data)

        return new_id
