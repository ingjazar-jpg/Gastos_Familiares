# Sistema de Control de Gastos Personales y Presupuesto Familiar

Aplicación web local para registrar y consultar los movimientos económicos del hogar, organizar presupuestos y dar seguimiento al comportamiento financiero familiar.

El proyecto está desarrollado con **Python, FastAPI, React y Vite**, siguiendo una arquitectura separada entre frontend y backend. Este repositorio contiene el código fuente, las pruebas y la documentación técnica del MVP.

## Objetivo

Centralizar el registro de ingresos y gastos, facilitar el control del presupuesto familiar y ofrecer información clara para apoyar la toma de decisiones sobre las finanzas del hogar.

## Funcionalidades

El MVP contempla seis módulos principales:

- **Dashboard:** resumen de la situación financiera y visualización de indicadores y gráficos.
- **Ingresos:** registro, consulta y administración de ingresos.
- **Gastos:** registro y administración de gastos.
- **Presupuestos:** definición y seguimiento de presupuestos, con alertas según los umbrales establecidos.
- **Historial:** consulta de movimientos y aplicación de filtros.
- **Papelera:** recuperación de registros eliminados y eliminación permanente.

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python, FastAPI y Pydantic |
| Frontend | React y Vite |
| Interfaz | HTML5, CSS3 y JavaScript |
| Gráficos | Recharts |
| Persistencia del MVP | Archivos JSON locales |
| Pruebas backend | Pytest |
| Calidad frontend | ESLint |

## Arquitectura

La solución separa la interfaz de usuario y la lógica de negocio:

- **Frontend React + Vite:** presenta los módulos, formularios, filtros, notificaciones y gráficos.
- **Backend FastAPI:** expone la API REST, valida los datos y ejecuta las reglas de negocio.
- **Repositorio JSON:** el backend lee y escribe los datos en `datos/datos_gastos.json`. El frontend no accede directamente al archivo.

Flujo general:

```text
React + Vite
    │
    │ Solicitudes HTTP (/api)
    ▼
FastAPI
    │
    ▼
Servicios y reglas de negocio
    │
    ▼
Repositorio JSON
    │
    ▼
datos/datos_gastos.json
```

## Estructura del repositorio

```text
sistema_gastos_familiar/
├── backend/
│   ├── app/
│   │   ├── api/             # Endpoints REST
│   │   ├── core/            # Configuración y dependencias
│   │   ├── models/          # Modelos del dominio
│   │   ├── repositories/    # Persistencia JSON
│   │   ├── schemas/         # Esquemas y validaciones
│   │   └── services/        # Lógica de negocio
│   └── tests/               # Pruebas del backend
├── datos/                   # Datos locales de la aplicación
├── docs/                    # Especificaciones y documentación técnica
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── styles/
│       └── utils/
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Requisitos previos

Para ejecutar el proyecto localmente se requiere:

- Python 3.10 o superior.
- Node.js compatible con Vite 8 (20.19+ o 22.12+).
- npm, incluido con Node.js.

## Instalación y ejecución local

Los siguientes pasos están escritos para **PowerShell en Windows**. Ejecuta los comandos desde la carpeta raíz del proyecto, `sistema_gastos_familiar`.

### 1. Preparar el backend

Crear y activar un entorno virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Iniciar el servidor FastAPI:

```powershell
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

El backend estará disponible en:

- API: http://127.0.0.1:8000
- Documentación interactiva: http://127.0.0.1:8000/docs
- Estado del servicio: http://127.0.0.1:8000/health

Al iniciar, el backend prepara el archivo local de datos si todavía no existe.

### 2. Preparar el frontend

Abre una segunda terminal de PowerShell y entra en la carpeta del frontend:

```powershell
cd frontend
npm install
npm run dev
```

Vite mostrará la dirección local para abrir la aplicación; normalmente es:

http://127.0.0.1:5173

El servidor de desarrollo del frontend está configurado para comunicarse con FastAPI mediante un proxy local para las rutas `/api`.

### 3. Detener los servicios

Para detener cada servidor, utiliza `Ctrl + C` en la terminal correspondiente. Para salir del entorno virtual de Python, ejecuta:

```powershell
deactivate
```

## Pruebas y validaciones

Desde la raíz del repositorio:

**Backend:**

```powershell
python -m pytest backend/tests
```

**Frontend – análisis estático:**

```powershell
cd frontend
npm run lint
```

**Frontend – compilación de producción:**

```powershell
npm run build
```

En la validación del MVP se registraron los siguientes resultados:

- **Backend:** 130 pruebas ejecutadas.
- **Frontend:** ESLint finalizado sin errores.
- **Compilación:** build de Vite completado correctamente.
- **Flujos revisados:** operaciones CRUD, cálculos del dashboard, presupuestos, alertas, filtros del historial y recuperación/eliminación de registros desde la papelera.

La compilación reportó una advertencia no bloqueante por el tamaño de un paquete JavaScript superior a 500 kB. La optimización mediante división de código queda como mejora futura.

## Datos y privacidad

- Los datos de la aplicación se almacenan localmente en `datos/datos_gastos.json`.
- Los archivos JSON de datos están excluidos del control de versiones mediante `.gitignore`; el repositorio conserva la carpeta con un archivo marcador.
- No se deben subir al repositorio datos financieros personales, archivos de entorno ni credenciales.
- La configuración de desarrollo utiliza interfaces locales (`127.0.0.1`); no está planteada como despliegue multiusuario o servicio público.

**Importante:** antes de utilizar la aplicación en producción o habilitar acceso multiusuario, será necesario evaluar una base de datos, autenticación y autorización, seguridad, copias de respaldo, recuperación y demás requisitos operativos.

## Estado del proyecto

**MVP funcional, validado y publicado en GitHub.**

El repositorio incluye el código fuente de backend y frontend, pruebas automatizadas y documentación técnica en la carpeta `docs/`.

## Mejoras futuras

- Evaluar la migración de persistencia a una base de datos.
- Incorporar autenticación y gestión de usuarios si se requiere acceso multiusuario.
- Consolidar la estrategia de copias de seguridad y recuperación.
- Optimizar la carga del frontend mediante división de código.

---

Proyecto desarrollado con Python, FastAPI, React y Vite.
