"""Representación de una gramática libre de contexto y su carga desde archivo."""

import os
import re

from .validador import (
    EPSILON,
    MARCAS_EPSILON,
    ErrorDeSintaxis,
    es_ignorable,
    validar_linea,
)

# Cuerpo vacío: se representa internamente como la tupla vacía ().
CUERPO_VACIO = ()


class Gramatica:
    """Gramática libre de contexto G = (V, T, P, S).

    Las producciones se guardan como un diccionario:
        { 'S': [('0','A','0'), ('1','B','1'), ('B','B')] }
    Cada cuerpo es una tupla de símbolos; la tupla vacía () representa ε.
    """

    def __init__(self, producciones=None, simbolo_inicial=None):
        self.producciones = producciones if producciones is not None else {}
        self.simbolo_inicial = simbolo_inicial
        self.orden = list(self.producciones.keys())

    # --- Consultas -----------------------------------------------------------
    @property
    def no_terminales(self):
        """Conjunto de no terminales (letras mayúsculas)."""
        encontrados = set(self.producciones.keys())
        for cuerpos in self.producciones.values():
            for cuerpo in cuerpos:
                encontrados.update(s for s in cuerpo if s.isupper())
        return encontrados

    @property
    def terminales(self):
        """Conjunto de terminales (minúsculas y dígitos)."""
        encontrados = set()
        for cuerpos in self.producciones.values():
            for cuerpo in cuerpos:
                encontrados.update(s for s in cuerpo if not s.isupper())
        return encontrados

    def agregar(self, cabeza, cuerpo):
        """Agrega una producción evitando duplicados."""
        if cabeza not in self.producciones:
            self.producciones[cabeza] = []
            self.orden.append(cabeza)
        if cuerpo not in self.producciones[cabeza]:
            self.producciones[cabeza].append(cuerpo)

    def total_producciones(self):
        return sum(len(cuerpos) for cuerpos in self.producciones.values())

    # --- Presentación --------------------------------------------------------
    @staticmethod
    def cuerpo_a_texto(cuerpo):
        return EPSILON if cuerpo == CUERPO_VACIO else "".join(cuerpo)

    def linea_de(self, cabeza):
        cuerpos = self.producciones.get(cabeza, [])
        derecha = " | ".join(self.cuerpo_a_texto(c) for c in cuerpos)
        return f"{cabeza} -> {derecha}"

    def __str__(self):
        return "\n".join(self.linea_de(c) for c in self.orden if self.producciones[c])


def _separar_simbolos(cuerpo_texto):
    """Convierte el texto de un cuerpo en una tupla de símbolos.

    '0A0' -> ('0', 'A', '0')      'ε' -> ()
    """
    if cuerpo_texto.lower() in MARCAS_EPSILON:
        return CUERPO_VACIO
    return tuple(cuerpo_texto)


def parsear_linea(linea):
    """Devuelve (cabeza, [cuerpos]) de una línea ya validada."""
    izquierda, derecha = re.split(r"->|→", linea, maxsplit=1)
    cabeza = izquierda.strip()
    cuerpos = [_separar_simbolos(p.strip()) for p in derecha.split("|")]
    return cabeza, cuerpos


def cargar_gramatica(ruta, verbose=True):
    """Lee un archivo de texto, valida cada línea y construye la gramática.

    Si alguna línea está mal escrita se lanza ErrorDeSintaxis y la ejecución
    del programa debe detenerse.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    gramatica = Gramatica()

    with open(ruta, "r", encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            linea = linea.rstrip("\n")

            if es_ignorable(linea):
                continue

            validar_linea(linea, numero)          # puede lanzar ErrorDeSintaxis
            if verbose:
                print(f"   línea {numero:>2} | OK  | {linea.strip()}")

            cabeza, cuerpos = parsear_linea(linea)
            for cuerpo in cuerpos:
                gramatica.agregar(cabeza, cuerpo)

            if gramatica.simbolo_inicial is None:
                gramatica.simbolo_inicial = cabeza

    if not gramatica.producciones:
        raise ErrorDeSintaxis(0, "el archivo no contiene producciones")

    return gramatica
