"""Pruebas unitarias: revisan las reglas de validacion de forma aislada.

No levantan el servidor ni tocan la base de datos: solo llaman a las
funciones y comparan lo que devuelven.
"""

import os
import sys
import unittest

os.environ["APP_ENV"] = "pruebas"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app


class PruebasDeValidacion(unittest.TestCase):

    def test_cp_u_01_nombre_vacio_produce_error(self):
        """CP-U-01: validar() rechaza el envio cuando falta el nombre."""
        errores = app.validar("", "ana@ejemplo.com", "Soporte", "Hola")
        self.assertIn("El nombre es obligatorio.", errores)
        self.assertEqual(len(errores), 1,
                         "solo deberia reportarse el error del nombre")

    def test_cp_u_02_correo_sin_dominio_valido(self):
        """CP-U-02: correo_valido() exige usuario y dominio con punto."""
        validos = ["ana@ejemplo.com", "juan.perez@unisalle.edu.co"]
        invalidos = ["ana@", "@ejemplo.com", "ana@b", "a@@b.com", "ana@b."]

        for correo in validos:
            self.assertTrue(app.correo_valido(correo),
                            f"{correo} deberia aceptarse")
        for correo in invalidos:
            self.assertFalse(app.correo_valido(correo),
                             f"{correo} deberia rechazarse")


if __name__ == "__main__":
    unittest.main(verbosity=2)
