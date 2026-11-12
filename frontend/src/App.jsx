
import { useState } from 'react'

import Sidebar from './components/layout/Sidebar'
import Topbar from './components/layout/Topbar'
import DashboardPage from './pages/DashboardPage'
import IngresosPage from './pages/IngresosPage'
import GastosPage from './pages/GastosPage'
import PresupuestosPage from './pages/PresupuestosPage'
import HistorialPage from './pages/HistorialPage'
import PapeleraPage from './pages/PapeleraPage'

import './App.css'

function App() {
  const fechaActual = new Date()

  const [seccionActiva, setSeccionActiva] = useState('Dashboard')
  const [mes, setMes] = useState(fechaActual.getMonth() + 1)
  const [anio, setAnio] = useState(fechaActual.getFullYear())

  const subtitulos = {
    Dashboard: 'Visualiza el comportamiento de tus finanzas familiares.',
    Ingresos: 'Administra el dinero que recibes.',
    Gastos: 'Controla los movimientos de dinero que realizas.',
    Presupuestos: 'Organiza y controla tus lÃ­mites de gasto.',
    Historial: 'Consulta tus movimientos financieros.',
    Papelera: 'Administra los registros eliminados.',
  }

  return (
    <div className="app-shell">
      <Sidebar
        seccionActiva={seccionActiva}
        onNavigate={setSeccionActiva}
      />

      <main className="main-area">
        <Topbar
          titulo={seccionActiva}
          subtitulo={subtitulos[seccionActiva]}
          mes={mes}
          anio={anio}
          onMesChange={setMes}
          onAnioChange={setAnio}
        />

        {seccionActiva === 'Dashboard' ? (
          <DashboardPage mes={mes} anio={anio} />
        ) : seccionActiva === 'Ingresos' ? (
          <IngresosPage mes={mes} anio={anio} />
        ) : seccionActiva === 'Gastos' ? (
          <GastosPage mes={mes} anio={anio} />
        ) : seccionActiva === 'Presupuestos' ? (
          <PresupuestosPage mes={mes} anio={anio} />
        ) : seccionActiva === 'Historial' ? (
          <HistorialPage mes={mes} anio={anio} />
        ) : seccionActiva === 'Papelera' ? (
          <PapeleraPage />
        ) : (
          <section className="placeholder-page">
            <div className="placeholder-icon">â–ª</div>
            <h2>{seccionActiva}</h2>
            <p>
              Esta secciÃ³n se habilitarÃ¡ en la siguiente etapa
              de implementaciÃ³n.
            </p>
            <button
              type="button"
              className="primary-button"
              onClick={() => setSeccionActiva('Dashboard')}
            >
              Volver al Dashboard
            </button>
          </section>
        )}
      </main>
    </div>
  )
}

export default App


