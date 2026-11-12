# 5. Reglas de negocio

**Versión:** 1.0

## 5.1 Períodos
- La aplicación administra movimientos por mes y año.
- El selector global de período se aplica a las vistas financieras pertinentes.
- Al iniciar, se propone mostrar el mes y año actuales.

## 5.2 Cálculos
Para un período seleccionado, usando exclusivamente registros activos:
- Ingresos totales = suma de ingresos.
- Gastos totales = suma de gastos.
- Saldo disponible = ingresos totales − gastos totales.
- Presupuesto disponible = presupuesto mensual − gastos totales.
- Porcentaje utilizado = gastos totales / presupuesto mensual × 100.

El presupuesto disponible puede ser negativo si los gastos superan el presupuesto.

## 5.3 Período sin presupuesto
- Mostrar literalmente `Sin presupuesto configurado`.
- Mantener visibles los ingresos y gastos reales.
- No calcular porcentaje de uso ni presupuesto disponible.
- No generar alertas presupuestarias.
- No representar un presupuesto inexistente como `$0`.

## 5.4 Estados y alertas
| Estado | Condición |
|---|---|
| `normal` | Uso inferior al 80 % |
| `advertencia` | Uso desde 80 % hasta exactamente 100 % |
| `excedido` | Uso superior al 100 % |
| `sin_presupuesto` | No existe presupuesto activo |

El Dashboard mantiene una alerta persistente según el estado actual. Los toast aparecen cuando una operación produce una transición de estado. Cambiar únicamente el período seleccionado no genera toast. No repetir toast mientras el estado no cambie.

## 5.5 Eliminación y papelera
- Eliminar desde una vista ordinaria marca `eliminado: true`.
- Los registros en papelera se excluyen de listas ordinarias, cálculos y gráficos.
- Restaurar conserva el ID y vuelve a incluir el registro en los cálculos.
- Restaurar presupuesto se rechaza con HTTP 409 si existe un presupuesto activo para el mismo mes/año.
- La eliminación permanente solo se permite desde la papelera y requiere confirmación explícita en la interfaz.
- La eliminación permanente no reduce contadores.

## 5.6 Categorías
Ingresos: Salario, Honorarios, Ventas, Inversiones, Otros.  
Gastos: Alimentación, Transporte, Servicios, Salud, Educación, Entretenimiento, Vivienda, Otros.

Las categorías son predefinidas y no editables por el usuario.
