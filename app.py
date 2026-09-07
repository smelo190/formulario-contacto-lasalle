from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import config

app = Flask(__name__)

ASUNTOS = ["Soporte", "Ventas", "Sugerencia", "Otro"]


def conectar():
    conexion = sqlite3.connect(config.BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
    conexion = conectar()
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            asunto TEXT,
            mensaje TEXT
        )
    """)
    conexion.commit()
    conexion.close()


def guardar(nombre, correo, asunto, mensaje):
    conexion = conectar()
    cursor = conexion.execute(
        "INSERT INTO mensajes (nombre, correo, asunto, mensaje) VALUES (?, ?, ?, ?)",
        (nombre, correo, asunto, mensaje)
    )
    conexion.commit()
    numero = cursor.lastrowid
    conexion.close()
    return numero


def validar(nombre, correo, asunto, mensaje):
    errores = []
    if nombre == "":
        errores.append("El nombre es obligatorio.")
    if correo == "":
        errores.append("El correo es obligatorio.")
    elif "@" not in correo:
        errores.append("El correo no tiene un formato valido.")
    if asunto == "":
        errores.append("Debe elegir un asunto.")
    if mensaje == "":
        errores.append("El mensaje es obligatorio.")
    return errores


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    errores = []
    datos = {"nombre": "", "correo": "", "asunto": "", "mensaje": ""}

    if request.method == "POST":
        datos["nombre"] = request.form["nombre"].strip()
        datos["correo"] = request.form["correo"].strip()
        datos["asunto"] = request.form["asunto"].strip()
        datos["mensaje"] = request.form["mensaje"].strip()

        errores = validar(datos["nombre"], datos["correo"], datos["asunto"], datos["mensaje"])

        if errores == []:
            numero = guardar(datos["nombre"], datos["correo"], datos["asunto"], datos["mensaje"])
            return redirect(url_for("confirmacion", numero=numero))

    return render_template("contacto.html", asuntos=ASUNTOS, errores=errores, datos=datos)


@app.route("/confirmacion/<numero>")
def confirmacion(numero):
    conexion = conectar()
    mensaje = conexion.execute("SELECT * FROM mensajes WHERE id = ?", (numero,)).fetchone()
    conexion.close()
    return render_template("confirmacion.html", mensaje=mensaje)


@app.route("/mensajes")
def mensajes():
    conexion = conectar()
    lista = conexion.execute("SELECT * FROM mensajes ORDER BY id DESC").fetchall()
    conexion.close()
    return render_template("mensajes.html", lista=lista, ambiente=config.AMBIENTE)


crear_tabla()

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
