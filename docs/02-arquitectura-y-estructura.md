# 2. Arquitectura y estructura

**Versión:** 1.0

## 2.1 Arquitectura lógica
La solución se divide en dos aplicaciones locales:

1. **Frontend React + Vite:** presentación, navegación, formularios, filtros, notificaciones y gráficos.
2. **Backend FastAPI:** API REST, validaciones, reglas de negocio, cálculos financieros y acceso exclusivo al archivo JSON.

Flujo de datos:

`React/Vite → API HTTP local → FastAPI → servicios/repositorios → datos_gastos.json`

El frontend no tendrá acceso directo al archivo JSON.

## 2.2 Tecnologías
- Python.
- FastAPI.
- Pydantic 2.
- React con Vite (JavaScript/JSX).
- HTML5 y CSS3.
- Recharts.
- JSON como persistencia local.
- Visual Studio Code como entorno de desarrollo.

## 2.3 Estructura prevista
```text
sistema_gastos_familiar/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   └── tests/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── styles/
│       └── utils/
├── datos/
├── docs/
└── README.md
```

## 2.4 Responsabilidades del backend
- Exponer endpoints REST bajo `/api`.
- Validar entradas mediante Pydantic 2.
- Generar identificadores secuenciales.
- Aplicar reglas de negocio y eliminación lógica.
- Calcular indicadores y datos para gráficos.
- Leer y escribir `datos/datos_gastos.json`.
- Crear el archivo de datos si no existe.

## 2.5 Responsabilidades del frontend
- Mostrar Dashboard, Ingresos, Gastos, Presupuestos, Historial y Papelera.
- Enviar y recibir información mediante la API.
- Formatear fechas y valores monetarios para presentación.
- Actualizar las vistas afectadas después de operaciones exitosas.
- Mostrar errores y confirmaciones comprensibles.
- Representar los gráficos usando datos entregados por el backend.

## 2.6 Restricción de ejecución local
La configuración de desarrollo deberá enlazar los servicios a interfaces locales y no habilitar acceso desde la red. La configuración CORS deberá limitarse al origen local utilizado por Vite.
