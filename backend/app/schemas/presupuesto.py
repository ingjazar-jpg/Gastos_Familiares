from pydantic import BaseModel, ConfigDict, Field


class PresupuestoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mes: int = Field(strict=True, ge=1, le=12)
    anio: int = Field(strict=True, ge=1000, le=9999)
    monto: int = Field(strict=True, gt=0)


class PresupuestoCreate(PresupuestoBase):
    pass


class PresupuestoUpdate(PresupuestoBase):
    pass


class PresupuestoResponse(PresupuestoBase):
    id: int = Field(strict=True, gt=0)
    eliminado: bool