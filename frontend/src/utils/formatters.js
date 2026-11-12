
const monedaCOP = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  maximumFractionDigits: 0,
})

const numeroCompacto = new Intl.NumberFormat('es-CO', {
  notation: 'compact',
  maximumFractionDigits: 1,
})

const nombresCategorias = {
  alimentacion: 'Alimentación',
  transporte: 'Transporte',
  servicios: 'Servicios',
  salud: 'Salud',
  educacion: 'Educación',
  entretenimiento: 'Entretenimiento',
  vivienda: 'Vivienda',
  salario: 'Salario',
  honorarios: 'Honorarios',
  ventas: 'Ventas',
  inversiones: 'Inversiones',
  otros: 'Otros',
}

export function formatearMoneda(valor) {
  return monedaCOP.format(valor ?? 0)
}

export function formatearNumeroCompacto(valor) {
  return `$${numeroCompacto.format(valor ?? 0)}`
}

export function formatearCategoria(categoria) {
  return nombresCategorias[categoria] ?? categoria
}
