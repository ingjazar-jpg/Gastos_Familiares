const API_BASE_URL = ''

async function solicitudAPI(endpoint, opciones = {}) {
  const respuesta = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...opciones,
    headers: {
      ...(opciones.body ? { 'Content-Type': 'application/json' } : {}),
      ...opciones.headers,
    },
  })

  const contenido = await respuesta.json().catch(() => null)

  if (!respuesta.ok) {
    let mensaje = `Error en la solicitud (${respuesta.status}).`

    if (typeof contenido?.detail === 'string') {
      mensaje = contenido.detail
    } else if (Array.isArray(contenido?.detail)) {
      mensaje = contenido.detail
        .map((error) => error.msg)
        .join('. ')
    }

    throw new Error(mensaje)
  }

  return contenido
}

// DASHBOARD

export async function obtenerDashboard(mes, anio) {
  const parametros = new URLSearchParams({
    mes: String(mes),
    anio: String(anio),
  })

  return solicitudAPI(
    `/api/dashboard?${parametros.toString()}`,
  )
}

// INGRESOS

export async function obtenerIngresos(mes, anio, categoria) {
  const parametros = new URLSearchParams()

  if (mes !== undefined && mes !== null) {
    parametros.set('mes', String(mes))
  }

  if (anio !== undefined && anio !== null) {
    parametros.set('anio', String(anio))
  }

  if (categoria) {
    parametros.set('categoria', categoria)
  }

  const consulta = parametros.toString()
  const endpoint = consulta
    ? `/api/ingresos?${consulta}`
    : '/api/ingresos'

  return solicitudAPI(endpoint)
}

export async function registrarIngreso(datos) {
  return solicitudAPI('/api/ingresos', {
    method: 'POST',
    body: JSON.stringify(datos),
  })
}

export async function actualizarIngreso(ingresoId, datos) {
  return solicitudAPI(`/api/ingresos/${ingresoId}`, {
    method: 'PUT',
    body: JSON.stringify(datos),
  })
}

export async function eliminarIngreso(ingresoId) {
  return solicitudAPI(`/api/ingresos/${ingresoId}`, {
    method: 'DELETE',
  })
}

// GASTOS

export async function obtenerGastos(mes, anio, categoria) {
  const parametros = new URLSearchParams()

  if (mes !== undefined && mes !== null) {
    parametros.set('mes', String(mes))
  }

  if (anio !== undefined && anio !== null) {
    parametros.set('anio', String(anio))
  }

  if (categoria) {
    parametros.set('categoria', categoria)
  }

  const consulta = parametros.toString()
  const endpoint = consulta
    ? `/api/gastos?${consulta}`
    : '/api/gastos'

  return solicitudAPI(endpoint)
}

export async function registrarGasto(datos) {
  return solicitudAPI('/api/gastos', {
    method: 'POST',
    body: JSON.stringify(datos),
  })
}

export async function actualizarGasto(gastoId, datos) {
  return solicitudAPI(`/api/gastos/${gastoId}`, {
    method: 'PUT',
    body: JSON.stringify(datos),
  })
}

export async function eliminarGasto(gastoId) {
  return solicitudAPI(`/api/gastos/${gastoId}`, {
    method: 'DELETE',
  })
}


export async function obtenerPresupuestos(mes, anio) {
  const parametros = new URLSearchParams()

  if (mes) parametros.append('mes', mes)
  if (anio) parametros.append('anio', anio)

  const consulta = parametros.toString()
  const endpoint = consulta
    ? `/api/presupuestos?${consulta}`
    : '/api/presupuestos'

  return solicitudAPI(endpoint)
}

export async function registrarPresupuesto(datos) {
  return solicitudAPI('/api/presupuestos', {
    method: 'POST',
    body: JSON.stringify(datos),
  })
}

export async function actualizarPresupuesto(presupuestoId, datos) {
  return solicitudAPI(`/api/presupuestos/${presupuestoId}`, {
    method: 'PUT',
    body: JSON.stringify(datos),
  })
}

export async function eliminarPresupuesto(presupuestoId) {
  return solicitudAPI(`/api/presupuestos/${presupuestoId}`, {
    method: 'DELETE',
  })
}

export async function obtenerHistorial(
  mes,
  anio,
  tipo,
  categoria
) {
  const parametros = new URLSearchParams()

  if (mes && anio) {
    parametros.append('mes', mes)
    parametros.append('anio', anio)
  }

  if (tipo) parametros.append('tipo', tipo)
  if (categoria) parametros.append('categoria', categoria)

  const consulta = parametros.toString()
  const endpoint = consulta
    ? `/api/historial?${consulta}`
    : '/api/historial'

  return solicitudAPI(endpoint)
}


export async function listarPapelera(tipo) {
  const parametros = new URLSearchParams()

  if (tipo) parametros.append('tipo', tipo)

  const consulta = parametros.toString()
  const endpoint = consulta
    ? `/api/papelera?${consulta}`
    : '/api/papelera'

  return solicitudAPI(endpoint)
}

export async function restaurarRegistro(tipo, registroId) {
  return solicitudAPI(
    `/api/papelera/${tipo}/${registroId}/restaurar`,
    {
      method: 'POST',
    }
  )
}

export async function eliminarPermanentemente(tipo, registroId) {
  return solicitudAPI(
    `/api/papelera/${tipo}/${registroId}`,
    {
      method: 'DELETE',
    }
  )
}
