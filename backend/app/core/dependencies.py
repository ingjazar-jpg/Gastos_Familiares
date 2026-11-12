
from backend.app.repositories.json_repository import JsonRepository


# Instancia compartida del repositorio de datos.
repository = JsonRepository()


def get_repository() -> JsonRepository:
    """
    Proporciona acceso al repositorio JSON compartido.

    Los servicios y las rutas de la API utilizarán esta dependencia
    para acceder a los datos mediante el backend.
    """
    return repository
