
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.core.dependencies import get_repository
from backend.app.api.ingresos import router as ingresos_router
from backend.app.api.gastos import router as gastos_router
from backend.app.api.presupuestos import router as presupuestos_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.historial import router as historial_router
from backend.app.api.papelera import router as papelera_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Inicializa los recursos necesarios al arrancar FastAPI.
    """
    repository = get_repository()
    repository.ensure_file()

    yield


app = FastAPI(
    title="Sistema de Control de Gastos Familiares",
    description=(
        "API local para la gestión de ingresos, "
        "gastos y presupuestos familiares."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(ingresos_router)
app.include_router(gastos_router)
app.include_router(presupuestos_router)
app.include_router(dashboard_router)
app.include_router(historial_router)
app.include_router(papelera_router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API del Sistema de Gastos Familiares funcionando correctamente",
        "estado": "activo",
    }


@app.get("/health")
def verificar_estado():
    return {
        "estado": "saludable",
        "servicio": "backend",
    }
