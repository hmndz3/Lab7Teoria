"""Programa principal del Laboratorio 7 - Simplificación de gramáticas.

Uso:
    python lab7.py gramaticas/gramatica1.txt
    python lab7.py gramaticas/gramatica1.txt --preservar-vacio
"""

import argparse
import sys

from .epsilon import eliminar_producciones_epsilon, encontrar_anulables
from .gramatica import Gramatica, cargar_gramatica
from .validador import ErrorDeSintaxis

ANCHO = 72


def titulo(texto):
    print("\n" + "=" * ANCHO)
    print(texto.center(ANCHO))
    print("=" * ANCHO)


def paso(numero, texto):
    print(f"\n[PASO {numero}] {texto}")
    print("-" * ANCHO)


def mostrar_gramatica(gramatica, sangria="   "):
    for cabeza in gramatica.orden:
        if gramatica.producciones[cabeza]:
            print(sangria + gramatica.linea_de(cabeza))


def ejecutar(ruta, preservar_vacio=False):
    titulo("LABORATORIO 7 - ELIMINACIÓN DE PRODUCCIONES-ε")
    print(f"Archivo de entrada: {ruta}")

    # ---------------- PASO 1: validación con expresión regular --------------
    paso(1, "Validando cada línea del archivo con la expresión regular")
    try:
        gramatica = cargar_gramatica(ruta)
    except ErrorDeSintaxis as error:
        print(f"   línea {error.numero_linea:>2} | ERROR | {error.contenido}")
        print("\n" + "!" * ANCHO)
        print("  La gramática NO es válida. Se detiene la ejecución.")
        print(f"  Motivo: {error}")
        print("!" * ANCHO)
        return 1
    except FileNotFoundError as error:
        print(f"   ERROR: {error}")
        return 1
    print("   Todas las líneas están bien escritas.")

    # ---------------- PASO 2: gramática cargada -----------------------------
    paso(2, "Gramática original")
    mostrar_gramatica(gramatica)
    print(f"\n   Símbolo inicial : {gramatica.simbolo_inicial}")
    print(f"   No terminales   : {{{', '.join(sorted(gramatica.no_terminales))}}}")
    print(f"   Terminales      : {{{', '.join(sorted(gramatica.terminales))}}}")
    print(f"   Producciones    : {gramatica.total_producciones()}")

    # ---------------- PASO 3: símbolos anulables ----------------------------
    paso(3, "Buscando los símbolos anulables (los que derivan ε)")

    def registrar_anulables(iteracion, conjunto, motivo):
        etiqueta = "base  " if iteracion == 0 else f"iter {iteracion}"
        actual = ", ".join(sorted(conjunto)) if conjunto else "vacío"
        print(f"   {etiqueta} | ANULABLES = {{{actual}}}")
        print(f"          | por: {motivo}")

    anulables = encontrar_anulables(gramatica, registrar=registrar_anulables)
    print(f"\n   Símbolos anulables: {{{', '.join(sorted(anulables))}}}")

    # ---------------- PASO 4: los 2^m casos ---------------------------------
    paso(4, "Generando las nuevas producciones (2^m casos por producción)")

    def registrar_combinaciones(cabeza, cuerpo, combinaciones, anulables_actuales):
        texto_cuerpo = "".join(cuerpo)
        m = sum(1 for s in cuerpo if s in anulables_actuales)
        marcados = "".join(
            f"[{s}]" if s in anulables_actuales else s for s in cuerpo
        )
        print(f"\n   {cabeza} -> {texto_cuerpo}   (anulables marcados: {marcados})")
        total = 2 ** m
        print(f"      m = {m}  =>  2^{m} = {total} {'caso' if total == 1 else 'casos'}")
        repetidos = total - len(combinaciones)
        if repetidos:
            plural = "caso genera" if repetidos == 1 else "casos generan"
            print(f"      ({repetidos} {plural} un cuerpo repetido, no se agrega dos veces)")
        for nuevo, decision in combinaciones:
            resultado = "".join(nuevo) if nuevo else "ε"
            quitados = [
                cuerpo[i] for i, conservar in sorted(decision.items()) if not conservar
            ]
            detalle = f"se quita {', '.join(quitados)}" if quitados else "no se quita nada"
            aviso = "" if nuevo else "  <- se descarta"
            print(f"      - {cabeza} -> {resultado:<10} ({detalle}){aviso}")

    nueva, anulables, descartadas = eliminar_producciones_epsilon(
        gramatica, registrar=registrar_combinaciones, preservar_vacio=preservar_vacio
    )

    if descartadas:
        print("\n   Producciones descartadas:")
        for cabeza, cuerpo, motivo in descartadas:
            texto = Gramatica.cuerpo_a_texto(cuerpo)
            print(f"      - {cabeza} -> {texto}: {motivo}")

    # ---------------- PASO 5: resultado -------------------------------------
    paso(5, "Gramática resultante SIN producciones-ε")
    mostrar_gramatica(nueva)
    print(f"\n   Símbolo inicial : {nueva.simbolo_inicial}")
    print(f"   Producciones    : {nueva.total_producciones()} "
          f"(antes eran {gramatica.total_producciones()})")

    if gramatica.simbolo_inicial in anulables and not preservar_vacio:
        print("\n   Nota: la gramática original generaba la cadena vacía.")
        print("   Use --preservar-vacio para agregar S0 -> S | ε y conservarla.")

    titulo("FIN")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Elimina las producciones-ε de una gramática libre de contexto."
    )
    parser.add_argument("archivo", help="ruta del archivo de texto con la gramática")
    parser.add_argument(
        "--preservar-vacio",
        action="store_true",
        help="agrega un nuevo símbolo inicial S0 -> S | ε si el lenguaje contenía ε",
    )
    args = parser.parse_args(argv)
    return ejecutar(args.archivo, args.preservar_vacio)


if __name__ == "__main__":
    sys.exit(main())
