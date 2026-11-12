
const meses = [
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

function Topbar({
  titulo,
  subtitulo,
  mes,
  anio,
  onMesChange,
  onAnioChange,
}) {
  const anioActual = new Date().getFullYear()
  const anios = Array.from(
    { length: 7 },
    (_, index) => anioActual - 3 + index,
  )

  return (
    <header className="topbar">
      <div className="topbar-heading">
        <span className="breadcrumb">FINANZAS / {titulo.toUpperCase()}</span>
        <h1>{titulo}</h1>
        <p>{subtitulo}</p>
      </div>

      <div className="period-selector">
        <span className="period-label">PERIODO</span>

        <div className="period-controls">
          <select
            aria-label="Mes seleccionado"
            value={mes}
            onChange={(event) => onMesChange(Number(event.target.value))}
          >
            {meses.map((nombre, index) => (
              <option key={nombre} value={index + 1}>
                {nombre}
              </option>
            ))}
          </select>

          <select
            aria-label="Año seleccionado"
            value={anio}
            onChange={(event) => onAnioChange(Number(event.target.value))}
          >
            {anios.map((valor) => (
              <option key={valor} value={valor}>
                {valor}
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  )
}

export default Topbar
