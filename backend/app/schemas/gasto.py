from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.app.models.categorias import CategoriaGasto


class GastoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    concepto: str = Field(min_length=1, max_length=100)
    categoria: CategoriaGasto
    monto: int = Field(strict=True, gt=0)
    fecha: date

    @field_validator("concepto")
    @classmethod
    def validar_concepto(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("El concepto no puede estar vacío.")

        return valor


class GastoCreate(GastoBase):
    pass


class GastoUpdate(GastoBase):
    pass


class GastoResponse(GastoBase):
    id: int = Field(strict=True, gt=0)
    eliminado: bool