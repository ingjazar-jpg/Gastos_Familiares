
import { useEffect, useState } from 'react'
import {
  listarPapelera,
  restaurarRegistro,
  eliminarPermanentemente,
} from '../services/api'
import {
  formatearMoneda,
  formatearCategoria,
} from '../utils/formatters'

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

function obtenerDetalle(registro) {
  if (registro.tipo === 'presupuesto') {
    return `Presupuesto de ${nombresMeses[registro.mes - 1]} ${registro.anio}`
  }

  return registro.concepto
}

function obtenerPeriodo(registro) {
  if (registro.tipo === 'presupuesto') {
    return `${nombresMeses[registro.mes - 1]} ${registro.anio}`
  }

  return formatearCategoria(registro.categoria)
}

function obtenerFecha(registro) {
  if (registro.tipo === 'presupuesto') {
    return '—'
  }

  return formatearFecha(registro.fecha)
}

function obtenerNombreTipo(tipo) {
  const nombres = {
    ingreso: 'Ingreso',
    gasto: 'Gasto',
    presupuesto: 'Presupuesto',
  }

  return nombres[tipo] || tipo
}

export default function PapeleraPage() {
  const [registros, setRegistros] = useState([])
  const [tipo, setTipo] = useState('')
  const [cargando, setCargando] = useState(true)
  const [registroEnProceso, setRegistroEnProceso] = useState('')
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  useEffect(() => {
    let vigente = true

    listarPapelera(tipo || undefined)
      .then((datos) => {
        if (vigente) {
          setRegistros(datos)
          setError('')
        }
      })
      .catch((err) => {
        if (vigente) {
          setError(
            err.message || 'No fue posible consultar la papelera.'
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
  }, [tipo])

  async function actualizarLista() {
    const datos = await listarPapelera(tipo || undefined)
    setRegistros(datos)
  }

  async function manejarRestauracion(registro) {
    const clave = `${registro.tipo}-${registro.id}`

    setRegistroEnProceso(clave)
    setError('')
    setMensaje('')

    try {
      const resultado = await restaurarRegistro(
        registro.tipo,
        registro.id
      )

      await actualizarLista()

      setMensaje(
        resultado.mensaje || 'Registro restaurado correctamente.'
      )
    } catch (err) {
      setError(
        err.message || 'No fue posible restaurar el registro.'
      )
    } finally {
      setRegistroEnProceso('')
    }
  }

  async function manejarEliminacion(registro) {
    const confirmar = window.confirm(
      `¿Deseas eliminar definitivamente este ${obtenerNombreTipo(registro.tipo).toLowerCase()}? Esta acción no se puede deshacer.`
    )

    if (!confirmar) return

    const clave = `${registro.tipo}-${registro.id}`

    setRegistroEnProceso(clave)
    setError('')
    setMensaje('')

    try {
      const resultado = await eliminarPermanentemente(
        registro.tipo,
        registro.id
      )

      await actualizarLista()

      setMensaje(
        resultado.mensaje || 'Registro eliminado permanentemente.'
      )
    } catch (err) {
      setError(
        err.message || 'No fue posible eliminar el registro.'
      )
    } finally {
      setRegistroEnProceso('')
    }
  }

  return (
    <section className="trash-page">
      <header className="trash-header">
        <div>
          <h1>Papelera</h1>
          <p>
            Consulta, recupera o elimina definitivamente los
            registros eliminados.
          </p>
        </div>
      </header>

      <section className="trash-card">
        <div className="trash-card-header">
          <h2>Registros eliminados</h2>

          <span className="trash-count">
            {registros.length} registros
          </span>
        </div>

        <div className="trash-filters">
          <div className="trash-field">
            <label htmlFor="trash-type">
              Tipo de registro
            </label>

            <select
              id="trash-type"
              value={tipo}
              onChange={(event) => {
                setTipo(event.target.value)
                setMensaje('')
                setError('')
              }}
            >
              <option value="">Todos</option>
              <option value="ingreso">Ingresos</option>
              <option value="gasto">Gastos</option>
              <option value="presupuesto">Presupuestos</option>
            </select>
          </div>
        </div>

        {mensaje && (
          <div className="trash-success" role="status">
            {mensaje}
          </div>
        )}

        {error && (
          <div className="trash-error" role="alert">
            {error}
          </div>
        )}

        {cargando ? (
          <p className="trash-empty">
            Cargando papelera...
          </p>
        ) : error && registros.length === 0 ? null : registros.length === 0 ? (
          <p className="trash-empty">
            No hay registros eliminados.
          </p>
        ) : (
          <div className="trash-table-wrapper">
            <table className="trash-table">
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Detalle</th>
                  <th>Categoría / Período</th>
                  <th>Fecha</th>
                  <th>Monto</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                {registros.map((registro) => {
                  const clave = `${registro.tipo}-${registro.id}`
                  const procesando = registroEnProceso === clave

                  return (
                    <tr key={clave}>
                      <td>
                        <span className={`trash-type trash-type-${registro.tipo}`}>
                          {obtenerNombreTipo(registro.tipo)}
                        </span>
                      </td>

                      <td>{obtenerDetalle(registro)}</td>

                      <td>{obtenerPeriodo(registro)}</td>

                      <td>{obtenerFecha(registro)}</td>

                      <td className="trash-amount">
                        {formatearMoneda(registro.monto)}
                      </td>

                      <td>
                        <div className="trash-actions">
                          <button
                            type="button"
                            className="trash-button trash-restore"
                            disabled={Boolean(registroEnProceso)}
                            onClick={() => manejarRestauracion(registro)}
                          >
                            {procesando ? 'Procesando...' : 'Recuperar'}
                          </button>

                          <button
                            type="button"
                            className="trash-button trash-delete"
                            disabled={Boolean(registroEnProceso)}
                            onClick={() => manejarEliminacion(registro)}
                          >
                            Eliminar
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  )
}
