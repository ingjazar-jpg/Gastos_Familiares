
const opciones = [
  { nombre: 'Dashboard', icono: '▦' },
  { nombre: 'Ingresos', icono: '↗' },
  { nombre: 'Gastos', icono: '↘' },
  { nombre: 'Presupuestos', icono: '◷' },
  { nombre: 'Historial', icono: '≡' },
  { nombre: 'Papelera', icono: '▢' },
]

function Sidebar({ seccionActiva, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-logo">GF</div>
        <div>
          <strong>Gastos Familiares</strong>
          <span>CONTROL FINANCIERO</span>
        </div>
      </div>

      <div className="sidebar-section-label">MENÚ PRINCIPAL</div>

      <nav className="sidebar-nav" aria-label="Navegación principal">
        {opciones.map((opcion) => (
          <button
            key={opcion.nombre}
            type="button"
            className={`nav-item ${
              seccionActiva === opcion.nombre ? 'active' : ''
            }`}
            onClick={() => onNavigate(opcion.nombre)}
            aria-current={
              seccionActiva === opcion.nombre ? 'page' : undefined
            }
          >
            <span className="nav-icon" aria-hidden="true">
              {opcion.icono}
            </span>
            <span>{opcion.nombre}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="connection-dot" />
        <div>
          <strong>Almacenamiento local</strong>
          <span>Conexión disponible</span>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
