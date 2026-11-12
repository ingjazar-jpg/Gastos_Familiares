
import { useEffect, useState } from 'react'
import { obtenerHistorial } from '../services/api'
import {
  formatearMoneda,
  formatearCategoria,
} from '../utils/formatters'

const categoriasIngresos = [
  'salario',
  'honorarios',
  'ventas',
  'inversiones',
  'otros',
]

const categoriasGastos = [
  'alimentacion',
  'transporte',
  'servicios',
  'salud',
  'educacion',
  'entretenimiento',
  'vivienda',
  'otros',
]

const categorias = [
  ...categoriasIngresos.filter((item) => item !== 'otros'),
  ...categoriasGastos.filter((item) => item !== 'otros'),
  'otros',
]

function formatearFecha(fecha) {
  if (!fecha) return '—'

  const fechaLocal = new Date(`${fecha}T00:00:00`)

  if (Number.isNaN(fechaLocal.getTime())) return fecha

  return new Intl.DateTimeFormat('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(fechaLocal)
}

export default function HistorialPage({ mes, anio }) {
  const [movimientos, setMovimientos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [tipo, setTipo] = useState('')
  const [categoria, setCategoria] = useState('')

  useEffect(() => {
    let vigente = true

    obtenerHistorial(
      mes,
      anio,
      tipo || undefined,
      categoria || undefined
    )
      .then((datos) => {
        if (vigente) {
          setMovimientos(datos)
          setError('')
        }
      })
      .catch((err) => {
        if (vigente) {
          setError(
            err.message || 'No fue posible consultar el historial.'
          )
        }
      })
      .finally(() => {
        if (vigente) {
          setCargando(false)
        }
      })

    return () => {
      vigente = false
    }
  }, [mes, anio, tipo, categoria])

  const categoriasDisponibles =
  tipo === 'ingreso'
    ? categoriasIngresos
    : tipo === 'gasto'
      ? categoriasGastos
      : categorias

  return (
    <section className="history-page">
      <header className="history-header">
        <div>
          <h1>Historial</h1>
          <p>Consulta tus ingresos y gastos registrados.</p>
        </div>
      </header>

      <section className="history-card">
        <div className="history-card-header">
          <h2>Movimientos registrados</h2>
          <span className="history-count">
            {movimientos.length} movimientos
          </span>
        </div>

        <div className="history-filters">
          <div className="history-field">
            <label htmlFor="history-type">Tipo de movimiento</label>
            <select
              id="history-type"
              value={tipo}
              onChange={(event) => {
                setTipo(event.target.value)
                setCategoria('')
                }}
            >
              <option value="">Todos</option>
              <option value="ingreso">Ingresos</option>
              <option value="gasto">Gastos</option>
            </select>
          </div>

          <div className="history-field">
            <label htmlFor="history-category">Categoría</label>
            <select
              id="history-category"
              value={categoria}
              onChange={(event) => setCategoria(event.target.value)}
            >
              <option value="">Todas</option>
              {categoriasDisponibles.map((item) => (
                <option key={item} value={item}>
                    {formatearCategoria(item)}
                </option>
            ))}
            </select>
          </div>
        </div>

        {error && (
          <div className="history-error" role="alert">
            {error}
          </div>
        )}

        {cargando ? (
          <p className="history-empty">Cargando historial...</p>
        ) : error ? null : movimientos.length === 0 ? (
          <p className="history-empty">
            No hay movimientos registrados para este período.
          </p>
        ) : (
          <div className="history-table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Concepto</th>
                  <th>Tipo</th>
                  <th>Categoría</th>
                  <th>Monto</th>
                </tr>
              </thead>

              <tbody>
                {movimientos.map((movimiento) => (
                  <tr key={`${movimiento.tipo}-${movimiento.id}`}>
                    <td>{formatearFecha(movimiento.fecha)}</td>
                    <td>{movimiento.concepto}</td>
                    <td>
                      <span
                        className={`history-type history-type-${movimiento.tipo}`}
                      >
                        {movimiento.tipo === 'ingreso'
                          ? 'Ingreso'
                          : 'Gasto'}
                      </span>
                    </td>
                    <td>
                      {formatearCategoria(movimiento.categoria)}
                    </td>
                    <td
                      className={`history-amount history-amount-${movimiento.tipo}`}
                    >
                      {formatearMoneda(movimiento.monto)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  )
}

