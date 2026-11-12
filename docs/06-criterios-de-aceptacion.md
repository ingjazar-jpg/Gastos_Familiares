# 6. Criterios de aceptación

**Versión:** 1.0  
**Estado:** Aprobados como línea base; pruebas pendientes de implementación y ejecución.

- **CA-01 — Crear ingreso:** dado un formulario válido, al guardar se crea un ingreso con ID generado por backend y estado activo.
- **CA-02 — Crear gasto:** dado un formulario válido, al guardar se crea un gasto con ID generado por backend y estado activo.
- **CA-03 — Editar movimiento:** al editar un ingreso o gasto activo, se actualizan todos sus campos editables y se recalculan las vistas afectadas.
- **CA-04 — Crear presupuesto:** se permite un presupuesto por mes/año; un segundo presupuesto activo para el mismo período devuelve 409.
- **CA-05 — Editar presupuesto:** se permite modificar el presupuesto si no genera duplicidad activa de período.
- **CA-06 — Cálculos:** el Dashboard presenta correctamente ingresos, gastos y saldo a partir de movimientos activos.
- **CA-07 — Sin presupuesto:** se muestra `Sin presupuesto configurado`; no se calculan porcentaje, disponible presupuestario ni alertas.
- **CA-08 — Alertas:** se aplican los umbrales menor de 80 %, desde 80 % hasta 100 % inclusive, y superior a 100 %. El Dashboard conserva la alerta actual; el toast solo aparece ante transición por operación, nunca por cambiar período.
- **CA-09 — Exceso presupuestario:** el presupuesto disponible puede mostrarse como valor negativo.
- **CA-10 — Historial:** se muestran ingresos y gastos activos con filtros por mes, año, tipo y categoría.
- **CA-11 — Gráficos:** se presenta distribución de gastos por categoría y comparación de ingresos/gastos con datos reales de API.
- **CA-12 — Eliminación lógica:** al eliminar un movimiento o presupuesto, pasa a papelera y deja de participar en listados ordinarios y cálculos.
- **CA-13 — Restauración:** al restaurar, el registro recupera su ID y estado activo; vuelve a cálculos y gráficos. Se valida conflicto de presupuesto.
- **CA-14 — Eliminación permanente:** se elimina definitivamente desde papelera con confirmación explícita.
- **CA-15 — Contadores:** los IDs son secuenciales por colección y nunca se reutilizan.
- **CA-16 — Persistencia:** los datos se conservan en JSON entre ejecuciones; el backend crea el archivo si no existe.
- **CA-17 — Interfaz adaptable:** navegación y vistas son utilizables en escritorio y móvil.

## Calidad y definición de terminado
Una historia se considera terminada cuando:
1. Cumple sus criterios de aceptación.
2. Incluye validaciones de entrada y manejo de errores.
3. Mantiene consistencia entre persistencia, API e interfaz.
4. Cuenta con pruebas automatizadas pertinentes.
5. La documentación correspondiente está actualizada.
6. Las pruebas se han ejecutado y sus resultados se registran; no basta con que estén escritas.

## Nota de verificación
En esta fase no se han ejecutado pruebas: todavía no existe implementación funcional.
