import { useEffect, useState } from 'react'

import {
  obtenerGastos,
  registrarGasto,
  actualizarGasto,
  eliminarGasto,
} from '../services/api'

import {
  formatearMoneda,
  formatearCategoria,
} from '../utils/formatters'

const categorias = [
  { valor: 'alimentacion', nombre: 'Alimentación' },
  { valor: 'transporte', nombre: 'Transporte' },
  { valor: 'servicios', nombre: 'Servicios' },
  { valor: 'salud', nombre: 'Salud' },
  { valor: 'educacion', nombre: 'Educación' },
  { valor: 'entretenimiento', nombre: 'Entretenimiento' },
  { valor: 'vivienda', nombre: 'Vivienda' },
  { valor: 'otros', nombre: 'Otros' },
]

function obtenerFechaActual() {
  const fecha = new Date()
  const anio = fecha.getFullYear()
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const dia = String(fecha.getDate()).padStart(2, '0')

  return `${anio}-${mes}-${dia}`
}

function formatearFecha(fecha) {
  if (!fecha) return ''

  const [anio, mes, dia] = fecha.split('-')
  return `${dia}/${mes}/${anio}`
}

function formularioInicial() {
  return {
    concepto: '',
    categoria: '',
    monto: '',
    fecha: obtenerFechaActual(),
  }
}

function GastosPage({ mes, anio }) {
  const [gastos, setGastos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [guardando, setGuardando] = useState(false)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  const [categoriaFiltro, setCategoriaFiltro] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [gastoEditando, setGastoEditando] = useState(null)
  const [formulario, setFormulario] = useState(formularioInicial)
  const [recarga, setRecarga] = useState(0)

  useEffect(() => {
    let vigente = true

    async function cargarGastos() {
      setCargando(true)
      setError('')

      try {
        const datos = await obtenerGastos(
          mes,
          anio,
          categoriaFiltro || undefined,
        )

        if (vigente) {
          setGastos(Array.isArray(datos) ? datos : [])
        }
      } catch (err) {
        if (vigente) {
          setGastos([])
          setError(err.message || 'No se pudieron cargar los gastos.')
        }
      } finally {
        if (vigente) {
          setCargando(false)
        }
      }
    }

    cargarGastos()

    return () => {
      vigente = false
    }
  }, [mes, anio, categoriaFiltro, recarga])

  function cambiarCampo(evento) {
    const { name, value } = evento.target

    setFormulario((actual) => ({
      ...actual,
      [name]: value,
    }))
  }

  function abrirFormulario() {
    setGastoEditando(null)
    setFormulario(formularioInicial())
    setError('')
    setMensaje('')
    setMostrarFormulario(true)
  }

  function editarGasto(gasto) {
    setGastoEditando(gasto)
    setFormulario({
      concepto: gasto.concepto,
      categoria: gasto.categoria,
      monto: String(gasto.monto),
      fecha: gasto.fecha,
    })
    setError('')
    setMensaje('')
    setMostrarFormulario(true)
  }

  function cerrarFormulario() {
    setMostrarFormulario(false)
    setGastoEditando(null)
    setFormulario(formularioInicial())
    setError('')
  }

  async function guardarGasto(evento) {
    evento.preventDefault()

    const monto = Number(formulario.monto)

    if (!formulario.concepto.trim()) {
      setError('Debes ingresar el concepto del gasto.')
      return
    }

    if (!Number.isInteger(monto) || monto <= 0) {
      setError('El monto debe ser un número entero mayor que cero.')
      return
    }

    setGuardando(true)
    setError('')
    setMensaje('')

    const datos = {
      concepto: formulario.concepto.trim(),
      categoria: formulario.categoria,
      monto,
      fecha: formulario.fecha,
    }

    try {
      if (gastoEditando) {
        await actualizarGasto(gastoEditando.id, datos)
        setMensaje('El gasto se actualizó correctamente.')
      } else {
        await registrarGasto(datos)
        setMensaje('El gasto se registró correctamente.')
      }

      cerrarFormulario()
      setRecarga((actual) => actual + 1)
    } catch (err) {
      setError(err.message || 'No se pudo guardar el gasto.')
    } finally {
      setGuardando(false)
    }
  }

  async function borrarGasto(gasto) {
    const confirmar = window.confirm(
      `¿Deseas eliminar el gasto "${gasto.concepto}"?`,
    )

    if (!confirmar) return

    setError('')
    setMensaje('')

    try {
      await eliminarGasto(gasto.id)
      setMensaje('El gasto se eliminó correctamente.')
      setRecarga((actual) => actual + 1)
    } catch (err) {
      setError(err.message || 'No se pudo eliminar el gasto.')
    }
  }

  return (
    <div className="expense-page">
      <section className="expense-toolbar">
        <div>
          <h2>Registro de gastos</h2>
          <p>Consulta y administra el dinero que recibes.</p>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={abrirFormulario}
        >
          Registrar gasto
        </button>
      </section>

      {error && (
        <div className="inline-error" role="alert">
          {error}
        </div>
      )}

      {mensaje && (
        <div className="expense-success" role="status">
          {mensaje}
        </div>
      )}

      {mostrarFormulario && (
        <section className="expense-form-section">
          <h3>{gastoEditando ? 'Editar gasto' : 'Nuevo gasto'}</h3>

          <form onSubmit={guardarGasto}>
            <div className="expense-form-grid">
              <label className="expense-field">
                <span>Concepto</span>
                <input
                  type="text"
                  name="concepto"
                  value={formulario.concepto}
                  onChange={cambiarCampo}
                  maxLength={100}
                  required
                  placeholder="Ej. Salario mensual"
                />
              </label>

              <label className="expense-field">
                <span>Categoría</span>
                <select
                  name="categoria"
                  value={formulario.categoria}
                  onChange={cambiarCampo}
                  required
                >
                  <option value="">Selecciona una categoría</option>
                  {categorias.map((categoria) => (
                    <option
                      key={categoria.valor}
                      value={categoria.valor}
                    >
                      {categoria.nombre}
                    </option>
                  ))}
                </select>
              </label>

              <label className="expense-field">
                <span>Monto (COP)</span>
                <input
                  type="number"
                  name="monto"
                  value={formulario.monto}
                  onChange={cambiarCampo}
                  min="1"
                  step="1"
                  required
                  placeholder="Ej. 2500000"
                />
              </label>

              <label className="expense-field">
                <span>Fecha</span>
                <input
                  type="date"
                  name="fecha"
                  value={formulario.fecha}
                  onChange={cambiarCampo}
                  required
                />
              </label>
            </div>

            <div className="expense-form-actions">
              <button
                type="button"
                className="secondary-button"
                onClick={cerrarFormulario}
                disabled={guardando}
              >
                Cancelar
              </button>

              <button
                type="submit"
                className="primary-button"
                disabled={guardando}
              >
                {guardando
                  ? 'Guardando...'
                  : gastoEditando
                    ? 'Guardar cambios'
                    : 'Registrar gasto'}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="expense-list-section">
        <div className="expense-list-header">
          <div>
            <h3>Gastos registrados</h3>
            <p>
              {gastos.length}{' '}
              {gastos.length === 1 ? 'registro' : 'registros'}
            </p>
          </div>

          <label className="expense-filter">
            <span>Filtrar por categoría</span>
            <select
              value={categoriaFiltro}
              onChange={(evento) => setCategoriaFiltro(evento.target.value)}
            >
              <option value="">Todas las categorías</option>
              {categorias.map((categoria) => (
                <option
                  key={categoria.valor}
                  value={categoria.valor}
                >
                  {categoria.nombre}
                </option>
              ))}
            </select>
          </label>
        </div>

        {cargando ? (
          <div className="expense-message">
            <span className="loading-spinner" />
            <p>Consultando gastos...</p>
          </div>
        ) : gastos.length === 0 ? (
          <div className="expense-empty">
            <h3>No hay gastos registrados</h3>
            <p>
              No se encontraron gastos para el periodo y los filtros
              seleccionados.
            </p>
          </div>
        ) : (
          <div className="expense-table-container">
            <table className="expense-table">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Concepto</th>
                  <th>Categoría</th>
                  <th>Monto</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                {gastos.map((gasto) => (
                  <tr key={gasto.id}>
                    <td>{formatearFecha(gasto.fecha)}</td>
                    <td>{gasto.concepto}</td>
                    <td>{formatearCategoria(gasto.categoria)}</td>
                    <td>{formatearMoneda(gasto.monto)}</td>
                    <td>
                      <div className="expense-row-actions">
                        <button
                          type="button"
                          className="expense-edit-button"
                          onClick={() => editarGasto(gasto)}
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="expense-delete-button"
                          onClick={() => borrarGasto(gasto)}
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
      </section>
    </div>
  )
}

export default GastosPage

