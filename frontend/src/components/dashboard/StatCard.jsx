
import { formatearMoneda } from '../../utils/formatters'

function StatCard({ titulo, valor, icono, variante, descripcion }) {
  return (
    <article className="stat-card">
      <div className="stat-card-top">
        <span className={`stat-icon ${variante}`}>{icono}</span>
        <span className="stat-period">Este periodo</span>
      </div>

      <p className="stat-title">{titulo}</p>

      <strong className="stat-value">
        {formatearMoneda(valor)}
      </strong>

      <span className="stat-description">{descripcion}</span>
    </article>
  )
}

export default StatCard
