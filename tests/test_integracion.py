"""Pruebas de integracion: revisan que el codigo y la base de datos
trabajen juntos correctamente.

Aqui si se escribe en disco, sobre la base del ambiente de pruebas.
"""

import importlib
import os
import sqlite3
import sys
import unittest

os.environ["APP_ENV"] = "pruebas"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import app


class PruebasDeIntegracion(unittest.TestCase):

    def setUp(self):
        """Deja la base del ambiente de pruebas vacia antes de cada caso."""
        app.crear_tabla()
        conexion = app.conectar()
        conexion.execute("DELETE FROM mensajes")
        conexion.execute("DELETE FROM sqlite_sequence WHERE name = 'mensajes'")
        conexion.commit()
        conexion.close()

    def test_cp_i_01_guardar_inserta_y_devuelve_numero(self):
        """CP-I-01: guardar() escribe el registro y devuelve su numero."""
        numero = app.guardar("Ana Gomez", "ana@ejemplo.com", "Soporte",
                             "No puedo entrar a la plataforma.")

        self.assertEqual(numero, 1, "el primer mensaje deberia ser el numero 1")

        conexion = app.conectar()
        fila = conexion.execute("SELECT * FROM mensajes WHERE id = ?",
                                (numero,)).fetchone()
        conexion.close()

        self.assertIsNotNone(fila, "el registro deberia existir en la base")
        self.assertEqual(fila["nombre"], "Ana Gomez")
        self.assertEqual(fila["correo"], "ana@ejemplo.com")
        self.assertIsNotNone(fila["fecha"], "deberia guardarse la fecha")

    def test_cp_i_02_cada_ambiente_usa_su_propia_base(self):
        """CP-I-02: lo escrito en pruebas no aparece en desarrollo."""
        archivos = {}
        for ambiente in ("desarrollo", "pruebas", "produccion"):
            os.environ["APP_ENV"] = ambiente
            importlib.reload(config)
            archivos[ambiente] = config.BASE_DATOS

        self.assertEqual(len(set(archivos.values())), 3,
                         "los tres ambientes deberian usar archivos distintos")

        os.environ["APP_ENV"] = "pruebas"
        importlib.reload(config)

        app.guardar("Marca de pruebas", "p@ejemplo.com", "Otro", "Solo en pruebas")

        otra = sqlite3.connect(archivos["desarrollo"])
        otra.execute("""CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, correo TEXT,
            asunto TEXT, mensaje TEXT, fecha TEXT)""")
        encontrados = otra.execute(
            "SELECT count(*) FROM mensajes WHERE nombre = ?",
            ("Marca de pruebas",)).fetchone()[0]
        otra.close()

        self.assertEqual(encontrados, 0,
                         "el mensaje de pruebas no deberia estar en desarrollo")


if __name__ == "__main__":
    unittest.main(verbosity=2)
