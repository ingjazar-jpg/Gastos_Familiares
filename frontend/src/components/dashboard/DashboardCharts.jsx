
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import {
  formatearCategoria,
  formatearMoneda,
  formatearNumeroCompacto,
} from '../../utils/formatters'

const colores = [
  'var(--color-chart-category-1)',
  'var(--color-chart-category-2)',
  'var(--color-chart-category-3)',
  'var(--color-chart-category-4)',
  'var(--color-chart-category-5)',
  'var(--color-chart-category-6)',
  'var(--color-chart-category-7)',
  'var(--color-chart-category-8)',
]

function EstadoVacio({ mensaje }) {
  return (
    <div className="chart-empty">
      <span>◈</span>
      <p>{mensaje}</p>
    </div>
  )
}

function DashboardCharts({ graficos }) {
  const gastos = graficos?.gastos_por_categoria ?? []
  const comparacion = graficos?.ingresos_vs_gastos ?? []

  const nombresTipos = {
    ingresos: 'Ingresos',
    gastos: 'Gastos',
  }

  return (
    <section className="charts-grid">
      <article className="chart-card">
        <div className="chart-heading">
          <div>
            <h3>Gastos por categoría</h3>
            <p>Distribución de los gastos del periodo</p>
          </div>
          <span className="chart-heading-icon">◉</span>
        </div>

        {gastos.length === 0 ? (
          <EstadoVacio mensaje="No hay gastos registrados en este periodo." />
        ) : (
          <>
            <div className="chart-content pie-content">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={gastos}
                    dataKey="total"
                    nameKey="categoria"
                    innerRadius={64}
                    outerRadius={100}
                    paddingAngle={3}
                    stroke="none"
                  >
                    {gastos.map((item, index) => (
                      <Cell
                        key={item.categoria}
                        fill={colores[index % colores.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(valor, nombre) => [
                      formatearMoneda(valor),
                      formatearCategoria(nombre),
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-legend">
              {gastos.map((item, index) => (
                <div className="legend-item" key={item.categoria}>
                  <span
                    className="legend-dot"
                    style={{ backgroundColor: colores[index % colores.length] }}
                  />
                  <span>{formatearCategoria(item.categoria)}</span>
                  <strong>{formatearMoneda(item.total)}</strong>
                </div>
              ))}
            </div>
          </>
        )}
      </article>

      <article className="chart-card">
        <div className="chart-heading">
          <div>
            <h3>Ingresos vs. gastos</h3>
            <p>Comparación de movimientos financieros</p>
          </div>
          <span className="chart-heading-icon">▥</span>
        </div>

        {comparacion.every((item) => item.total === 0) ? (
          <EstadoVacio mensaje="Aún no hay movimientos financieros." />
        ) : (
          <div className="chart-content">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={comparacion}
                margin={{ top: 12, right: 10, left: 4, bottom: 8 }}
              >
                <CartesianGrid
                  stroke="var(--color-chart-grid)"
                  strokeDasharray="4 4"
                  vertical={false}
                />
                <XAxis
                  dataKey="tipo"
                  tickFormatter={(valor) => nombresTipos[valor] ?? valor}
                  tick={{ fill: 'var(--color-chart-label)', fontSize: 12 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tickFormatter={formatearNumeroCompacto}
                  tick={{ fill: 'var(--color-chart-label)', fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  width={65}
                />
                <Tooltip
                  formatter={(valor) => [
                    formatearMoneda(valor),
                    'Total',
                  ]}
                  labelFormatter={(valor) => nombresTipos[valor] ?? valor}
                  cursor={{ fill: 'var(--color-chart-cursor)' }}
                />
                <Bar
                  dataKey="total"
                  fill="var(--color-chart-income)"
                  radius={[7, 7, 0, 0]}
                  maxBarSize={76}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </article>
    </section>
  )
}

export default DashboardCharts

