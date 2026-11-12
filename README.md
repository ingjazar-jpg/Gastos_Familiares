# Sistema de Control de Gastos Personales y Presupuesto Familiar

Aplicación web local para registrar y consultar los movimientos económicos del hogar, organizar presupuestos y mantener un seguimiento del comportamiento financiero familiar.

## Objetivo

Centralizar el registro de ingresos y gastos, facilitar el control del presupuesto familiar y ofrecer información clara para apoyar la toma de decisiones sobre las finanzas del hogar.

## Funcionalidades

El MVP contempla seis módulos principales:

- **Dashboard:** resumen de la situación financiera y visualización de indicadores.
- **Ingresos:** registro, consulta y administración de ingresos.
- **Gastos:** registro y administración de gastos.
- **Presupuestos:** definición y seguimiento de presupuestos, con alertas según los umbrales establecidos.
- **Historial:** consulta de movimientos y aplicación de filtros.
- **Papelera:** recuperación de registros eliminados y eliminación permanente.

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python y FastAPI |
| Frontend | React y Vite |
| Persistencia del MVP | Archivos JSON locales |

## Arquitectura general

La solución separa la interfaz de usuario y la lógica de negocio:

- El frontend React presenta los módulos y permite la interacción con el sistema.
- El backend FastAPI gestiona las operaciones y reglas de negocio.
- La persistencia del MVP utiliza archivos JSON locales.

## Validación del MVP

En la validación funcional y técnica del proyecto se registraron los siguientes resultados:

- **Backend:** 130 pruebas ejecutadas.
- **Frontend:** validación de ESLint sin errores.
- **Compilación:** proceso de build de Vite completado correctamente.
- **Flujos revisados:** operaciones CRUD, cálculos del dashboard, presupuestos, alertas, filtros del historial y recuperación/eliminación de registros desde la papelera.

La compilación de producción reportó una advertencia no bloqueante por el tamaño de un paquete JavaScript superior a 500 kB. La optimización mediante división de código queda como mejora futura.

## Estado del proyecto

**MVP funcional y validado para ejecución local.**

La persistencia basada en archivos JSON está orientada al alcance local del MVP. Antes de utilizar la aplicación como servicio multiusuario o desplegarla en producción, será necesario evaluar una base de datos, controles de acceso, seguridad, estrategia de copias de respaldo y demás requisitos operativos.

## Mejoras futuras

- Evaluar la migración de persistencia a una base de datos.
- Reforzar seguridad y gestión de usuarios si se requiere acceso multiusuario.
- Consolidar la estrategia de copias de seguridad y recuperación.
- Optimizar la carga del frontend mediante división de código.

## Código fuente

Este repositorio contiene actualmente la documentación inicial del proyecto. El código fuente de backend y frontend todavía no se ha incorporado al repositorio.

---

Proyecto desarrollado con Python, FastAPI, React y Vite.
