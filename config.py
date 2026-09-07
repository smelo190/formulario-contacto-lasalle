import os

AMBIENTE = os.environ.get("APP_ENV", "desarrollo")

if AMBIENTE == "desarrollo":
    DEBUG = True
    BASE_DATOS = "contactos_desarrollo.db"

elif AMBIENTE == "pruebas":
    DEBUG = False
    BASE_DATOS = "contactos_pruebas.db"

else:
    DEBUG = False
    BASE_DATOS = "contactos_produccion.db"
