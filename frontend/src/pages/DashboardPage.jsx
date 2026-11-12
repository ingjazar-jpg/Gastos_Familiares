
import { useEffect, useState } from 'react'

import DashboardCharts from '../components/dashboard/DashboardCharts'
import StatCard from '../components/dashboard/StatCard'
import { obtenerDashboard } from '../services/api'
import { formatearMoneda } from '../utils/formatters'

function DashboardPage({ mes, anio }) {
  const [dashboard, setDashboard] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [intento, setIntento] = useState(0)

  useEffect(() => {
    let vigente = true

    async function consultar() {
      setCargando(true)
      setError('')

      try {
        const datos = await obtenerDashboard(mes, anio)

        if (vigente) {
          setDashboard(datos)
        }
      } catch (err) {
        if (vigente) {
          setDashboard(null)
          setError(err.message || 'No se pudo cargar el Dashboard.')
        }
      } finally {
        if (vigente) {
          setCargando(false)
        }
      }
    }

    consultar()

    return () => {
      vigente = false
    }
  }, [mes, anio, intento])

  if (cargando && !dashboard) {
    return (
      <div className="dashboard-message">
        <span className="loading-spinner" />
        <p>Consultando información financiera...</p>
      </div>
    )
  }

  if (error && !dashboard) {
    return (
      <div className="dashboard-message error-message">
        <span>!</span>
        <h2>No se pudo cargar la información</h2>
        <p>{error}</p>
        <button
            type="button"
            className="primary-button"
            onClick={() => setIntento((actual) => actual + 1)}
        >
            Volver a intentar
        </button>
      </div>
    )
  }

  const resumen = dashboard?.resumen
  const presupuesto = dashboard?.presupuesto

  const estadoPresupuesto = {
    normal: 'Dentro del presupuesto',
    advertencia: 'Presupuesto próximo al límite',
    excedido: 'Presupuesto excedido',
    sin_presupuesto: 'Sin presupuesto configurado',
  }

  const porcentaje = presupuesto?.porcentaje_ejecucion
  const porcentajeVisual = Math.min(Math.max(porcentaje ?? 0, 0), 100)

  return (
    <div className="dashboard-page">
      {error && (
        <div className="inline-error" role="alert">
          {error}
        </div>
      )}

      <section className="dashboard-intro">
        <div>
          <h2>Resumen financiero</h2>
          <p>Conoce el estado de tus finanzas durante el periodo seleccionado.</p>
        </div>
        <span className="data-indicator">
          <span />
          Datos actualizados desde tu almacenamiento local
        </span>
      </section>

      <section className="stats-grid">
        <StatCard
          titulo="Ingresos totales"
          valor={resumen.total_ingresos}
          icono="↗"
          variante="income"
          descripcion="Dinero recibido en el periodo"
        />

        <StatCard
          titulo="Gastos totales"
          valor={resumen.total_gastos}
          icono="↘"
          variante="expense"
          descripcion="Dinero utilizado en el periodo"
        />

        <StatCard
          titulo="Balance del periodo"
          valor={resumen.balance}
          icono="＝"
          variante="balance"
          descripcion="Ingresos menos gastos"
        />
      </section>

      <section className="budget-card">
        <div className="budget-heading">
          <div>
            <span className="section-eyebrow">CONTROL DEL PRESUPUESTO</span>
            <h3>Presupuesto mensual</h3>
          </div>

          <span className={`budget-status ${presupuesto.estado}`}>
            {estadoPresupuesto[presupuesto.estado] ?? presupuesto.estado}
          </span>
        </div>

        {!presupuesto.configurado ? (
          <div className="no-budget">
            <span className="no-budget-icon">◷</span>
            <div>
              <strong>Sin presupuesto configurado</strong>
              <p>
                No hay un presupuesto activo para el periodo seleccionado.
              </p>
            </div>
          </div>
        ) : (
          <>
            <div className="budget-values">
              <div>
                <span>Presupuesto establecido</span>
                <strong>{formatearMoneda(presupuesto.monto)}</strong>
              </div>
              <div>
                <span>Presupuesto disponible</span>
                <strong className={presupuesto.disponible < 0 ? 'negative' : ''}>
                  {formatearMoneda(presupuesto.disponible)}
                </strong>
              </div>
              <div>
                <span>Ejecución presupuestaria</span>
                <strong>{porcentaje}%</strong>
              </div>
            </div>

            <div
              className="budget-progress"
              role="progressbar"
              aria-label="Ejecución presupuestaria"
              aria-valuenow={Math.min(porcentaje, 100)}
              aria-valuemin="0"
              aria-valuemax="100"
            >
              <div
                className={`budget-progress-fill ${presupuesto.estado}`}
                style={{ width: `${porcentajeVisual}%` }}
              />
            </div>

            {presupuesto.estado === 'excedido' && (
              <p className="budget-alert">
                Los gastos superan el presupuesto establecido.
              </p>
            )}
          </>
        )}
      </section>

      <DashboardCharts graficos={dashboard.graficos} />

      {cargando && (
        <div className="refresh-indicator">Actualizando información...</div>
      )}
    </div>
  )
}

export default DashboardPage
