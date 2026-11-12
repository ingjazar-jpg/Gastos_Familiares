import { useEffect, useState } from 'react'

import {
  obtenerIngresos,
  registrarIngreso,
  actualizarIngreso,
  eliminarIngreso,
} from '../services/api'

import {
  formatearMoneda,
  formatearCategoria,
} from '../utils/formatters'

const categorias = [
  { valor: 'salario', nombre: 'Salario' },
  { valor: 'honorarios', nombre: 'Honorarios' },
  { valor: 'ventas', nombre: 'Ventas' },
  { valor: 'inversiones', nombre: 'Inversiones' },
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

function IngresosPage({ mes, anio }) {
  const [ingresos, setIngresos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [guardando, setGuardando] = useState(false)
  const [error, setError] = useState('')
  const [mensaje, setMensaje] = useState('')

  const [categoriaFiltro, setCategoriaFiltro] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [ingresoEditando, setIngresoEditando] = useState(null)
  const [formulario, setFormulario] = useState(formularioInicial)
  const [recarga, setRecarga] = useState(0)

  useEffect(() => {
    let vigente = true

    async function cargarIngresos() {
      setCargando(true)
      setError('')

      try {
        const datos = await obtenerIngresos(
          mes,
          anio,
          categoriaFiltro || undefined,
        )

        if (vigente) {
          setIngresos(Array.isArray(datos) ? datos : [])
        }
      } catch (err) {
        if (vigente) {
          setIngresos([])
          setError(err.message || 'No se pudieron cargar los ingresos.')
        }
      } finally {
        if (vigente) {
          setCargando(false)
        }
      }
    }

    cargarIngresos()

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
    setIngresoEditando(null)
    setFormulario(formularioInicial())
    setError('')
    setMensaje('')
    setMostrarFormulario(true)
  }

  function editarIngreso(ingreso) {
    setIngresoEditando(ingreso)
    setFormulario({
      concepto: ingreso.concepto,
      categoria: ingreso.categoria,
      monto: String(ingreso.monto),
      fecha: ingreso.fecha,
    })
    setError('')
    setMensaje('')
    setMostrarFormulario(true)
  }

  function cerrarFormulario() {
    setMostrarFormulario(false)
    setIngresoEditando(null)
    setFormulario(formularioInicial())
    setError('')
  }

  async function guardarIngreso(evento) {
    evento.preventDefault()

    const monto = Number(formulario.monto)

    if (!formulario.concepto.trim()) {
      setError('Debes ingresar el concepto del ingreso.')
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
      if (ingresoEditando) {
        await actualizarIngreso(ingresoEditando.id, datos)
        setMensaje('El ingreso se actualizó correctamente.')
      } else {
        await registrarIngreso(datos)
        setMensaje('El ingreso se registró correctamente.')
      }

      cerrarFormulario()
      setRecarga((actual) => actual + 1)
    } catch (err) {
      setError(err.message || 'No se pudo guardar el ingreso.')
    } finally {
      setGuardando(false)
    }
  }

  async function borrarIngreso(ingreso) {
    const confirmar = window.confirm(
      `¿Deseas eliminar el ingreso "${ingreso.concepto}"?`,
    )

    if (!confirmar) return

    setError('')
    setMensaje('')

    try {
      await eliminarIngreso(ingreso.id)
      setMensaje('El ingreso se eliminó correctamente.')
      setRecarga((actual) => actual + 1)
    } catch (err) {
      setError(err.message || 'No se pudo eliminar el ingreso.')
    }
  }

  return (
    <div className="income-page">
      <section className="income-toolbar">
        <div>
          <h2>Registro de ingresos</h2>
          <p>Consulta y administra el dinero que recibes.</p>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={abrirFormulario}
        >
          Registrar ingreso
        </button>
      </section>

      {error && (
        <div className="inline-error" role="alert">
          {error}
        </div>
      )}

      {mensaje && (
        <div className="income-success" role="status">
          {mensaje}
        </div>
      )}

      {mostrarFormulario && (
        <section className="income-form-section">
          <h3>{ingresoEditando ? 'Editar ingreso' : 'Nuevo ingreso'}</h3>

          <form onSubmit={guardarIngreso}>
            <div className="income-form-grid">
              <label className="income-field">
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

              <label className="income-field">
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

              <label className="income-field">
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

              <label className="income-field">
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

            <div className="income-form-actions">
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
                  : ingresoEditando
                    ? 'Guardar cambios'
                    : 'Registrar ingreso'}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="income-list-section">
        <div className="income-list-header">
          <div>
            <h3>Ingresos registrados</h3>
            <p>
              {ingresos.length}{' '}
              {ingresos.length === 1 ? 'registro' : 'registros'}
            </p>
          </div>

          <label className="income-filter">
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
          <div className="income-message">
            <span className="loading-spinner" />
            <p>Consultando ingresos...</p>
          </div>
        ) : ingresos.length === 0 ? (
          <div className="income-empty">
            <h3>No hay ingresos registrados</h3>
            <p>
              No se encontraron ingresos para el periodo y los filtros
              seleccionados.
            </p>
          </div>
        ) : (
          <div className="income-table-container">
            <table className="income-table">
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
                {ingresos.map((ingreso) => (
                  <tr key={ingreso.id}>
                    <td>{formatearFecha(ingreso.fecha)}</td>
                    <td>{ingreso.concepto}</td>
                    <td>{formatearCategoria(ingreso.categoria)}</td>
                    <td>{formatearMoneda(ingreso.monto)}</td>
                    <td>
                      <div className="income-row-actions">
                        <button
                          type="button"
                          className="income-edit-button"
                          onClick={() => editarIngreso(ingreso)}
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="income-delete-button"
                          onClick={() => borrarIngreso(ingreso)}
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

export default IngresosPage
