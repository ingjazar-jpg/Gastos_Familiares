# 4. Contratos API

**Versión:** 1.0  
**Prefijo:** `/api`  
**Formato:** JSON

## 4.1 Ingresos
| Método | Ruta | Comportamiento |
|---|---|---|
| GET | `/api/ingresos` | Lista ingresos activos; filtros opcionales `mes`, `anio`, `categoria` |
| POST | `/api/ingresos` | Crea ingreso; responde 201 |
| PUT | `/api/ingresos/{id}` | Reemplaza todos los campos editables |
| DELETE | `/api/ingresos/{id}` | Eliminación lógica |

## 4.2 Gastos
| Método | Ruta | Comportamiento |
|---|---|---|
| GET | `/api/gastos` | Lista gastos activos; filtros opcionales `mes`, `anio`, `categoria` |
| POST | `/api/gastos` | Crea gasto; responde 201 |
| PUT | `/api/gastos/{id}` | Reemplaza todos los campos editables |
| DELETE | `/api/gastos/{id}` | Eliminación lógica |

## 4.3 Presupuestos
| Método | Ruta | Comportamiento |
|---|---|---|
| GET | `/api/presupuestos` | Lista presupuestos activos; filtros opcionales `mes`, `anio` |
| POST | `/api/presupuestos` | Crea presupuesto; responde 201; duplicado activo: 409 |
| PUT | `/api/presupuestos/{id}` | Actualiza presupuesto; conflicto de período: 409 |
| DELETE | `/api/presupuestos/{id}` | Eliminación lógica |

## 4.4 Dashboard
`GET /api/dashboard?mes={mes}&anio={anio}`

Ambos parámetros son obligatorios. Respuesta conceptual:
```json
{
  "periodo": {"mes": 11, "anio": 2026},
  "indicadores": {
    "ingresos_totales": 2500000,
    "gastos_totales": 1200000,
    "saldo_disponible": 1300000,
    "presupuesto_mensual": 2000000,
    "presupuesto_disponible": 800000,
    "porcentaje_presupuesto_utilizado": 60
  },
  "estado_presupuesto": "normal",
  "graficos": {
    "distribucion_gastos": [
      {"categoria": "alimentacion", "total": 500000}
    ],
    "comparacion": {"ingresos": 2500000, "gastos": 1200000}
  }
}
```
Cuando no hay presupuesto, `presupuesto_mensual`, `presupuesto_disponible` y `porcentaje_presupuesto_utilizado` serán `null`, y `estado_presupuesto` será `sin_presupuesto`.

## 4.5 Historial
`GET /api/historial`

Filtros opcionales: `mes`, `anio`, `tipo` (`ingreso` o `gasto`) y `categoria`. Devuelve movimientos activos unificados, incluyendo el tipo de movimiento. Orden descendente por fecha; en igualdad de fecha, ID descendente dentro de cada tipo.

## 4.6 Papelera
| Método | Ruta | Comportamiento |
|---|---|---|
| GET | `/api/papelera` | Lista eliminados; filtro opcional `tipo` |
| POST | `/api/papelera/{tipo}/{id}/restaurar` | Restaura el registro original |
| DELETE | `/api/papelera/{tipo}/{id}` | Elimina permanentemente un registro de la papelera |

Tipos admitidos: `ingreso`, `gasto`, `presupuesto`.

## 4.7 Códigos HTTP
- `200`: operación correcta.
- `201`: recurso creado.
- `400`: solicitud no válida por regla de negocio, cuando corresponda.
- `404`: registro inexistente.
- `409`: conflicto, por ejemplo presupuesto duplicado o restauración incompatible.
- `422`: validación de datos.
- `500`: error interno.

Los errores de negocio deben incluir un mensaje comprensible en `detail`.
