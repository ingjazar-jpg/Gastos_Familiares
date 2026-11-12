# 7. Registro de decisiones aprobadas

**Versión:** 1.0

| ID | Decisión aprobada |
|---|---|
| D-01 | Uso personal, un usuario, sin autenticación ni multiusuario. |
| D-02 | IDs secuenciales numéricos generados por backend, nunca reutilizados. |
| D-03 | COP en pesos enteros, sin decimales. |
| D-04 | Fechas ISO `YYYY-MM-DD`; presentación `DD/MM/YYYY`. |
| D-05 | Un presupuesto general por mes/año; editable; papelera para eliminados. |
| D-06 | Alertas en Dashboard y toast; umbrales 80 % y más de 100 %. |
| D-07 | Recharts; gráfico de distribución de gastos y comparación ingresos/gastos. |
| D-08 | Persistencia JSON directa; creación automática; sin backup automático ni escritura atómica. |
| D-09 | Edición de ingresos, gastos y presupuestos; recálculo de vistas. |
| D-10 | Eliminación lógica y restauración desde papelera. |
| D-11 | Sin presupuesto: mostrar `Sin presupuesto configurado`; no calcular porcentaje ni alertas. |
| D-12 | Restauración completa con el mismo ID; validar conflictos de presupuesto. |
| D-13 | Sidebar: Dashboard, Ingresos, Gastos, Presupuestos, Historial y Papelera. |
| D-14 | Diseño ejecutivo/minimalista; paleta corporativa azul, blanco y grises, con colores semánticos. |
| D-15 | Sin campo de observaciones; formularios con concepto, categoría, monto y fecha. |
| D-16 | Aplicación local, sin acceso desde otros dispositivos ni Internet. |
| D-17 | Ingresos categorizados: salario, honorarios, ventas, inversiones y otros. |
| D-18 | Historial unificado con filtros por mes, año, tipo y categoría. |
| D-19 | Disponible presupuestario = presupuesto − gastos; puede ser negativo. |
| D-20 | Toast solo ante transición de estado; sin repetición en el mismo estado. |
| D-21 | Papelera con restauración y eliminación permanente confirmada. |
| D-22 | Categorías predefinidas, no editables por el usuario. |

## Paleta visual de referencia
- Azul corporativo: `#17365D`
- Azul secundario: `#3478C8`
- Blanco: `#FFFFFF`
- Gris claro: `#F3F5F8`
- Verde positivo: `#23865B`
- Ámbar de advertencia: `#D89A32`
