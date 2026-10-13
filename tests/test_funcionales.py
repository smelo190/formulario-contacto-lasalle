"""Pruebas funcionales: recorren la aplicacion como lo haria una persona,
usando el cliente de pruebas de Flask en lugar del navegador.
"""

import os
import sys
import unittest

os.environ["APP_ENV"] = "pruebas"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app


class PruebasFuncionales(unittest.TestCase):

    def setUp(self):
        self.cliente = app.app.test_client()
        app.crear_tabla()
        conexion = app.conectar()
        conexion.execute("DELETE FROM mensajes")
        conexion.execute("DELETE FROM sqlite_sequence WHERE name = 'mensajes'")
        conexion.commit()
        conexion.close()

    def test_cp_f_01_envio_correcto_llega_a_confirmacion(self):
        """CP-F-01: un envio valido redirige a la confirmacion con su numero."""
        respuesta = self.cliente.post("/contacto", data={
            "nombre": "Santiago Melo",
            "correo": "santiago@ejemplo.com",
            "asunto": "Soporte",
            "mensaje": "Prueba funcional del envio correcto."})

        self.assertEqual(respuesta.status_code, 302,
                         "deberia redirigir tras un envio correcto")
        self.assertIn("/confirmacion/1", respuesta.headers["Location"])

        pagina = self.cliente.get("/confirmacion/1").get_data(as_text=True)
        self.assertIn("Mensaje enviado", pagina)
        self.assertIn("Santiago Melo", pagina)

    def test_cp_f_02_confirmacion_inexistente_responde_404(self):
        """CP-F-02: consultar un numero que no existe no debe simular exito."""
        respuesta = self.cliente.get("/confirmacion/9999")

        self.assertEqual(respuesta.status_code, 404,
                         "un mensaje inexistente deberia dar 404, no 200")
        self.assertNotIn("Mensaje enviado", respuesta.get_data(as_text=True),
                         "no deberia mostrarse una confirmacion vacia")


if __name__ == "__main__":
    unittest.main(verbosity=2)
