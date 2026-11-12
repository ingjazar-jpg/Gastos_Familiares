# 1. Visión y alcance

**Proyecto:** Sistema de Control de Gastos Personales y Presupuesto Familiar  
**Versión:** 1.0

## 1.1 Objetivo
Disponer de una aplicación web local que permita registrar y consultar ingresos y gastos, definir un presupuesto mensual general y visualizar el comportamiento financiero mediante indicadores, alertas e informes gráficos.

## 1.2 Usuarios
- Un único usuario.
- Uso personal desde el mismo equipo.
- No se requiere inicio de sesión, roles ni gestión multiusuario.

## 1.3 Alcance funcional del MVP
- Registro, consulta, edición y eliminación lógica de ingresos.
- Registro, consulta, edición y eliminación lógica de gastos.
- Creación, consulta, edición y eliminación lógica de un presupuesto general por mes/año.
- Dashboard con totales, saldo, presupuesto disponible y estado de consumo.
- Alertas visuales y notificaciones toast ante cambios de estado del presupuesto.
- Historial unificado de ingresos y gastos con filtros.
- Papelera con restauración y eliminación permanente.
- Gráficos de distribución de gastos y comparación de ingresos frente a gastos.

## 1.4 Fuera de alcance
- Autenticación, perfiles y múltiples usuarios.
- Acceso remoto, publicación en Internet o despliegue en la nube.
- Integración bancaria o importación automática de movimientos.
- Presupuestos independientes por categoría.
- Creación o personalización de categorías.
- Base de datos externa y copias de seguridad automáticas.

## 1.5 Plataforma y moneda
- Aplicación ejecutada localmente.
- Moneda: pesos colombianos (COP).
- Los importes se almacenan como enteros positivos; no se admiten centavos.
- Presentación monetaria colombiana, por ejemplo `$250.000`.

## 1.6 Criterio general de éxito
La información persistida, los listados, los indicadores, las alertas y los gráficos deben reflejar consistentemente los movimientos activos del período seleccionado.
