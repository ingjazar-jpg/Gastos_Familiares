
import { useCallback, useEffect, useState } from 'react'

import {
  obtenerPresupuestos,
  registrarPresupuesto,
  actualizarPresupuesto,
  eliminarPresupuesto,
} from '../services/api'

import { formatearMoneda } from '../utils/formatters'

function PresupuestosPage({ mes, anio }) {
  const fechaActual = new Date()

  const [presupuestos, setPresupuestos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [guardando, setGuardando] = useState(false)
  const [presupuestoEditando, setPresupuestoEditando] = useState(null)

  const [formulario, setFormulario] = useState({
    mes: mes || fechaActual.getMonth() + 1,
    anio: anio || fechaActual.getFullYear(),
    monto: '',
  })

  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

 
  const cargarPresupuestos = useCallback(async () => {
    try {
      const datos = await obtenerPresupuestos(mes, anio)
      setPresupuestos(datos)
    } catch (err) {
      setError(err.message || 'No fue posible consultar los presupuestos.')
    } finally {
      setCargando(false)
    }
  }, [mes, anio, setPresupuestos, setError, setCargando])

 
  useEffect(() => {
    let vigente = true

    obtenerPresupuestos(mes, anio)
      .then((datos) => {
        if (vigente) {
          setPresupuestos(datos)
        }
      })
      .catch((err) => {
        if (vigente) {
          setError(
            err.message || 'No fue posible consultar los presupuestos.'
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
  }, [mes, anio])


  const manejarCambio = (evento) => {
    const { name, value } = evento.target

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  const limpiarFormulario = () => {
    setFormulario({
      mes: mes || fechaActual.getMonth() + 1,
      anio: anio || fechaActual.getFullYear(),
      monto: '',
    })

    setPresupuestoEditando(null)
    setError('')
  }

  const manejarEdicion = (presupuesto) => {
    setFormulario({
      mes: presupuesto.mes,
      anio: presupuesto.anio,
      monto: presupuesto.monto,
    })

    setPresupuestoEditando(presupuesto.id)
    setError('')
    setMensaje('')
  }

  const manejarEnvio = async (evento) => {
    evento.preventDefault()

    setError('')
    setMensaje('')

    const datos = {
      mes: Number(formulario.mes),
      anio: Number(formulario.anio),
      monto: Number(formulario.monto),
    }

    if (
      !Number.isInteger(datos.mes) ||
      datos.mes < 1 ||
      datos.mes > 12 ||
      !Number.isInteger(datos.anio) ||
      datos.anio < 1000 ||
      datos.anio > 9999 ||
      !Number.isInteger(datos.monto) ||
      datos.monto <= 0
    ) {
      setError('Verifica el mes, año y monto ingresados.')
      return
    }

    try {
      setGuardando(true)

      if (presupuestoEditando !== null) {
        await actualizarPresupuesto(presupuestoEditando, datos)
        setMensaje('Presupuesto actualizado correctamente.')
      } else {
        await registrarPresupuesto(datos)
        setMensaje('Presupuesto registrado correctamente.')
      }

      limpiarFormulario()
      await cargarPresupuestos()
    } catch (err) {
      setError(
        err.message ||
        'No fue posible guardar el presupuesto. Verifica los datos.'
      )
    } finally {
      setGuardando(false)
    }
  }

  const manejarEliminacion = async (presupuesto) => {
    const confirmar = window.confirm(
      `¿Deseas eliminar el presupuesto de ${presupuesto.mes}/${presupuesto.anio}?`
    )

    if (!confirmar) return

    setError('')
    setMensaje('')

    try {
      await eliminarPresupuesto(presupuesto.id)

      setMensaje('Presupuesto eliminado correctamente.')

      if (presupuestoEditando === presupuesto.id) {
        limpiarFormulario()
      }

      await cargarPresupuestos()
    } catch (err) {
      setError(err.message || 'No fue posible eliminar el presupuesto.')
    }
  }

  const nombresMeses = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre',
  ]

  return (
    <section className="budget-page">
      <div className="budget-header">
        <div>
          <h1>Presupuestos</h1>
          <p>
            Administra el presupuesto general de cada período mensual.
          </p>
        </div>
      </div>

      {mensaje && (
        <div className="budget-success" role="status">
          {mensaje}
        </div>
      )}

      {error && (
        <div className="budget-error" role="alert">
          {error}
        </div>
      )}

      <div className="budget-management-card">
        <div className="budget-management-card-header">
          <h2>
            {presupuestoEditando !== null
              ? 'Editar presupuesto'
              : 'Registrar presupuesto'}
          </h2>
        </div>

        <form className="budget-form" onSubmit={manejarEnvio}>
          <div className="budget-grid">
            <div className="budget-field">
              <label htmlFor="budget-mes">Mes</label>
              <select
                id="budget-mes"
                name="mes"
                value={formulario.mes}
                onChange={manejarCambio}
                required
              >
                {nombresMeses.map((nombre, indice) => (
                  <option key={indice + 1} value={indice + 1}>
                    {nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="budget-field">
              <label htmlFor="budget-anio">Año</label>
              <input
                id="budget-anio"
                type="number"
                name="anio"
                min="1000"
                max="9999"
                step="1"
                value={formulario.anio}
                onChange={manejarCambio}
                required
              />
            </div>

            <div className="budget-field">
              <label htmlFor="budget-monto">Monto (COP)</label>
              <input
                id="budget-monto"
                type="number"
                name="monto"
                min="1"
                step="1"
                placeholder="Ej. 2500000"
                value={formulario.monto}
                onChange={manejarCambio}
                required
              />
            </div>
          </div>

          <div className="budget-actions">
            <button
              type="submit"
              className="budget-button budget-button-primary"
              disabled={guardando}
            >
              {guardando
                ? 'Guardando...'
                : presupuestoEditando !== null
                  ? 'Guardar cambios'
                  : 'Registrar presupuesto'}
            </button>

            {presupuestoEditando !== null && (
              <button
                type="button"
                className="budget-button budget-button-secondary"
                onClick={limpiarFormulario}
                disabled={guardando}
              >
                Cancelar edición
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="budget-card">
        <div className="budget-management-card-header">
          <h2>Presupuestos registrados</h2>
          <span className="budget-count">
            {presupuestos.length} registros
          </span>
        </div>

        {cargando ? (
          <p className="budget-empty">Cargando presupuestos...</p>
        ) : presupuestos.length === 0 ? (
          <p className="budget-empty">
            No hay presupuestos registrados para este período.
          </p>
        ) : (
          <div className="budget-table-wrapper">
            <table className="budget-table">
              <thead>
                <tr>
                  <th>Período</th>
                  <th>Monto asignado</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                {presupuestos.map((presupuesto) => (
                  <tr key={presupuesto.id}>
                    <td>
                      {nombresMeses[presupuesto.mes - 1]}{' '}
                      {presupuesto.anio}
                    </td>

                    <td>
                      {formatearMoneda(presupuesto.monto)}
                    </td>

                    <td>
                      <div className="budget-row-actions">
                        <button
                          type="button"
                          className="budget-button budget-button-secondary"
                          onClick={() => manejarEdicion(presupuesto)}
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="budget-button budget-button-danger"
                          onClick={() => manejarEliminacion(presupuesto)}
                        >
                          Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  )
}

export default PresupuestosPage
