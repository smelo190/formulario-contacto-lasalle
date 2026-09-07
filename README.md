@'
# Formulario de contacto

Aplicacion web hecha con Flask y SQLite. Registra mensajes de contacto y
funciona en tres ambientes: desarrollo, pruebas y produccion.

## Requisitos

Python 3 instalado.

## Instalacion

    py -m pip install -r requirements.txt

## Configuracion

El ambiente se elige con la variable de entorno APP_ENV. El archivo
.env.example lista las variables disponibles y sus valores posibles.
El proyecto no maneja contrasenas, claves ni datos sensibles.

## Ejecucion

En PowerShell, desde la carpeta del proyecto:

    py app.py

    $env:APP_ENV = "pruebas"
    py app.py

    $env:APP_ENV = "produccion"
    py app.py

La aplicacion queda en http://127.0.0.1:5000

El valor de APP_ENV dura mientras la terminal este abierta. Al abrir una
terminal nueva, la aplicacion vuelve a arrancar en desarrollo.

## Como probar la aplicacion

1. Arranque en el ambiente de pruebas.
2. Entre a /contacto y envie el formulario con los cuatro campos correctos.
   Debe aparecer la pagina de confirmacion con el numero asignado.
3. Envie el formulario con el campo nombre vacio. Debe volver con el error
   y conservar lo que ya habia escrito en los otros campos.
4. Envie el formulario con el correo ana@b. Debe rechazarlo por formato.
5. Escriba un nombre de mas de 80 caracteres. Debe rechazarlo por largo.
6. Entre a /mensajes: debe aparecer solo el mensaje del paso 2, con su fecha.
7. Arranque en desarrollo y entre a /mensajes. La lista debe ser distinta,
   porque cada ambiente usa su propia base de datos.

## Diferencias entre ambientes

| Ambiente    | DEBUG | Base de datos            |
|-------------|-------|--------------------------|
| desarrollo  | True  | contactos_desarrollo.db  |
| pruebas     | False | contactos_pruebas.db     |
| produccion  | False | contactos_produccion.db  |

Los archivos .db se crean solos al arrancar y estan excluidos del
repositorio por el .gitignore.

## Validaciones

- Los cuatro campos son obligatorios.
- El correo debe tener una arroba, usuario, y dominio con punto.
- Largos maximos: nombre 80, correo 120, asunto 40, mensaje 1000 caracteres.
'@ | Set-Content -Encoding UTF8 README.md