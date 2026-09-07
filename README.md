# Formulario de contacto

Aplicacion web sencilla hecha con Flask y SQLite. Registra mensajes de contacto
y funciona en tres ambientes: desarrollo, pruebas y produccion.

## Instalacion

    py -m pip install -r requirements.txt

## Ejecucion

Desarrollo (es el ambiente por defecto):

    py app.py

Pruebas:

    $env:APP_ENV = "pruebas"
    py app.py

Produccion:

    $env:APP_ENV = "produccion"
    py app.py

La aplicacion queda en http://127.0.0.1:5000

Para volver a desarrollo, cierre la terminal y abra una nueva.

## Diferencias entre ambientes

| Ambiente    | DEBUG | Base de datos              |
|-------------|-------|----------------------------|
| desarrollo  | True  | contactos_desarrollo.db    |
| pruebas     | False | contactos_pruebas.db       |
| produccion  | False | contactos_produccion.db    |

Cada ambiente usa su propia base de datos, por lo que los mensajes de uno
no aparecen en los otros.
