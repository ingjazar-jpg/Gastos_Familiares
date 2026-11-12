# 3. Modelos de datos

**Versión:** 1.0

## 3.1 Convenciones
- Identificadores: enteros positivos, secuenciales y generados por el backend.
- Contadores independientes para ingresos, gastos y presupuestos.
- Los identificadores no se reutilizan, incluso después de una eliminación permanente.
- Importes: enteros positivos en COP.
- Fechas: `YYYY-MM-DD`.
- Eliminación lógica: campo `eliminado` booleano.

## 3.2 Ingreso
```json
{
  "id": 1,
  "concepto": "Salario mensual",
  "categoria": "salario",
  "monto": 2500000,
  "fecha": "2026-11-01",
  "eliminado": false
}
```
- `concepto`: texto obligatorio, no vacío, máximo 100 caracteres.
- `categoria`: `salario`, `honorarios`, `ventas`, `inversiones` u `otros`.
- `monto`: entero positivo.
- `fecha`: fecha válida ISO.
- `eliminado`: booleano.

## 3.3 Gasto
```json
{
  "id": 1,
  "concepto": "Mercado semanal",
  "categoria": "alimentacion",
  "monto": 180000,
  "fecha": "2026-11-03",
  "eliminado": false
}
```
Categorías: `alimentacion`, `transporte`, `servicios`, `salud`, `educacion`, `entretenimiento`, `vivienda`, `otros`.

## 3.4 Presupuesto
```json
{
  "id": 1,
  "mes": 11,
  "anio": 2026,
  "monto": 3000000,
  "eliminado": false
}
```
- `mes`: entero entre 1 y 12.
- `anio`: año de cuatro dígitos.
- `monto`: entero positivo.
- Solo puede existir un presupuesto activo por combinación mes/año.

## 3.5 Archivo JSON y contadores
```json
{
  "contadores": {
    "ingresos": 1,
    "gastos": 1,
    "presupuestos": 1
  },
  "ingresos": [],
  "gastos": [],
  "presupuestos": []
}
```
Cada contador representa el siguiente ID disponible. Al crear un registro se asigna el valor actual y luego se incrementa. Los contadores nunca disminuyen.

## 3.6 Reglas de integridad
- El cliente no envía `id` ni `eliminado` al crear o actualizar.
- El backend genera el ID y controla el estado de eliminación.
- Los registros eliminados no participan en listados ordinarios ni cálculos.
- Restaurar conserva el ID original.
- Restaurar un presupuesto genera conflicto si ya existe otro presupuesto activo para ese período.
