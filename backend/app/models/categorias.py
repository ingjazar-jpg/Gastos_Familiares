from enum import Enum


class CategoriaIngreso(str, Enum):
    SALARIO = "salario"
    HONORARIOS = "honorarios"
    VENTAS = "ventas"
    INVERSIONES = "inversiones"
    OTROS = "otros"


class CategoriaGasto(str, Enum):
    ALIMENTACION = "alimentacion"
    TRANSPORTE = "transporte"
    SERVICIOS = "servicios"
    SALUD = "salud"
    EDUCACION = "educacion"
    ENTRETENIMIENTO = "entretenimiento"
    VIVIENDA = "vivienda"
    OTROS = "otros"