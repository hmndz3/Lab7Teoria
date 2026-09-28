"""Validación de producciones de una gramática usando expresiones regulares.

Convención del laboratorio:
  - Una letra MAYÚSCULA individual  -> no terminal.
  - Una letra minúscula o un dígito -> terminal.
  - La cadena vacía se escribe como 'ε' (o la palabra 'epsilon').
  - Una línea puede tener varios cuerpos separados por el operador OR '|'.

Ejemplo de línea válida:
    S -> 0A0 | 1B1 | BB
"""

import re

# Marcadores aceptados para la cadena vacía.
EPSILON = "ε"
MARCAS_EPSILON = ("ε", "epsilon", "&")

# --- Piezas de la expresión regular ------------------------------------------
_SIMBOLO = r"[A-Za-z0-9]"                 # un terminal o un no terminal
_VACIO = r"(?:ε|epsilon|&)"               # la cadena vacía
_CUERPO = rf"(?:{_VACIO}|{_SIMBOLO}+)"    # un cuerpo de producción
_FLECHA = r"(?:->|→)"

# Producción completa: NoTerminal -> cuerpo ( | cuerpo )*
PATRON_PRODUCCION = re.compile(
    rf"^\s*[A-Z]\s*{_FLECHA}\s*{_CUERPO}(?:\s*\|\s*{_CUERPO})*\s*$"
)

# Se ignoran líneas en blanco y comentarios que inician con '#'.
PATRON_IGNORAR = re.compile(r"^\s*(#.*)?$")


class ErrorDeSintaxis(Exception):
    """Se lanza cuando una línea del archivo no es una producción válida."""

    def __init__(self, numero_linea, contenido):
        self.numero_linea = numero_linea
        self.contenido = contenido
        super().__init__(
            f"Línea {numero_linea}: producción mal escrita -> {contenido!r}"
        )


def es_ignorable(linea):
    """True si la línea está vacía o es un comentario."""
    return bool(PATRON_IGNORAR.match(linea))


def es_produccion_valida(linea):
    """True si la línea cumple con el formato de una producción."""
    return bool(PATRON_PRODUCCION.match(linea))


def validar_linea(linea, numero_linea):
    """Valida una línea; lanza ErrorDeSintaxis si está mal escrita."""
    if not es_produccion_valida(linea):
        raise ErrorDeSintaxis(numero_linea, linea.strip())
    return True
