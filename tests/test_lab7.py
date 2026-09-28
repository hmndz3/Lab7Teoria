"""Pruebas unitarias del Laboratorio 7."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.epsilon import (  # noqa: E402
    combinaciones_de_cuerpo,
    eliminar_producciones_epsilon,
    encontrar_anulables,
)
from src.gramatica import cargar_gramatica, parsear_linea  # noqa: E402
from src.validador import ErrorDeSintaxis, es_produccion_valida  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAMATICAS = os.path.join(RAIZ, "gramaticas")


class PruebasValidador(unittest.TestCase):
    def test_producciones_validas(self):
        validas = [
            "S -> 0A0 | 1B1 | BB",
            "C -> S | ε",
            "A->aAb|ε",
            "  S   ->   ABaC  ",
            "S → aSa | b",
        ]
        for linea in validas:
            self.assertTrue(es_produccion_valida(linea), linea)

    def test_producciones_invalidas(self):
        invalidas = [
            "s -> a",          # la cabeza debe ser mayúscula
            "AB -> a",         # la cabeza debe ser un solo símbolo
            "S -> ",           # falta el cuerpo
            "S -> a |",        # OR sin cuerpo a la derecha
            "S -> | a",        # OR sin cuerpo a la izquierda
            "S - > a",         # flecha mal escrita
            "S a b",           # sin flecha
            "S -> a$b",        # símbolo no permitido
        ]
        for linea in invalidas:
            self.assertFalse(es_produccion_valida(linea), linea)


class PruebasParser(unittest.TestCase):
    def test_parseo(self):
        self.assertEqual(
            parsear_linea("S -> 0A0 | 1B1 | BB"),
            ("S", [("0", "A", "0"), ("1", "B", "1"), ("B", "B")]),
        )

    def test_epsilon_es_tupla_vacia(self):
        self.assertEqual(parsear_linea("C -> S | ε"), ("C", [("S",), ()]))

    def test_archivo_invalido_detiene(self):
        ruta = os.path.join(GRAMATICAS, "gramatica_con_error.txt")
        with self.assertRaises(ErrorDeSintaxis):
            cargar_gramatica(ruta, verbose=False)


class PruebasAnulables(unittest.TestCase):
    def test_gramatica1(self):
        g = cargar_gramatica(os.path.join(GRAMATICAS, "gramatica1.txt"), verbose=False)
        self.assertEqual(encontrar_anulables(g), {"S", "A", "B", "C"})

    def test_gramatica2(self):
        g = cargar_gramatica(os.path.join(GRAMATICAS, "gramatica2.txt"), verbose=False)
        self.assertEqual(encontrar_anulables(g), {"S", "A", "B", "C", "D"})


class PruebasCombinaciones(unittest.TestCase):
    def test_cantidad_de_casos(self):
        # ABaC con A, B, C anulables -> m = 3 -> 2^3 = 8 casos
        combinaciones = combinaciones_de_cuerpo(("A", "B", "a", "C"), {"A", "B", "C"})
        self.assertEqual(len(combinaciones), 8)

    def test_sin_anulables(self):
        combinaciones = combinaciones_de_cuerpo(("a", "b"), set())
        self.assertEqual([c for c, _ in combinaciones], [("a", "b")])


class PruebasEliminacion(unittest.TestCase):
    def test_resultado_gramatica1(self):
        g = cargar_gramatica(os.path.join(GRAMATICAS, "gramatica1.txt"), verbose=False)
        nueva, _, _ = eliminar_producciones_epsilon(g)
        self.assertEqual(
            str(nueva),
            "S -> 0A0 | 00 | 1B1 | 11 | BB | B\nA -> C\nB -> S | A\nC -> S",
        )

    def test_resultado_gramatica2(self):
        g = cargar_gramatica(os.path.join(GRAMATICAS, "gramatica2.txt"), verbose=False)
        nueva, _, _ = eliminar_producciones_epsilon(g)
        self.assertEqual(
            str(nueva),
            "S -> aAa | aa | bBb | bb\n"
            "A -> C | a\nB -> C | b\nC -> CDE | CE | DE | E\nD -> A | B | ab",
        )

    def test_no_quedan_producciones_epsilon(self):
        for archivo in ("gramatica1.txt", "gramatica2.txt"):
            g = cargar_gramatica(os.path.join(GRAMATICAS, archivo), verbose=False)
            nueva, _, _ = eliminar_producciones_epsilon(g)
            for cuerpos in nueva.producciones.values():
                self.assertNotIn((), cuerpos)

    def test_preservar_cadena_vacia(self):
        g = cargar_gramatica(os.path.join(GRAMATICAS, "gramatica1.txt"), verbose=False)
        nueva, _, _ = eliminar_producciones_epsilon(g, preservar_vacio=True)
        self.assertEqual(nueva.simbolo_inicial, "S0")
        self.assertIn((), nueva.producciones["S0"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
