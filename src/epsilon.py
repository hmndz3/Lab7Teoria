"""Eliminación de producciones-ε de una gramática libre de contexto.

El algoritmo tiene dos etapas:

  1. Encontrar los símbolos anulables (los que derivan la cadena vacía):
        - Base:     A es anulable si existe A -> ε
        - Inducción: A es anulable si existe A -> X1 X2 ... Xk
                     y todos los Xi ya son anulables.
       Se repite hasta que el conjunto ya no cambie (punto fijo).

  2. Para cada producción A -> X1 ... Xk que tenga m símbolos anulables,
     se generan las 2^m combinaciones posibles (cada símbolo anulable se
     conserva o se elimina) y se descartan los cuerpos vacíos resultantes.

Las producciones unarias que puedan aparecer (por ejemplo S -> S) NO se tocan
aquí: eliminarlas es un paso posterior de la simplificación.
"""

from itertools import product

from .gramatica import CUERPO_VACIO, Gramatica


def encontrar_anulables(gramatica, registrar=None):
    """Devuelve el conjunto de símbolos anulables.

    'registrar' es una función opcional que recibe (iteracion, conjunto, motivo)
    para poder mostrar en pantalla el avance del algoritmo.
    """
    anulables = set()

    # --- Base: producciones A -> ε ---
    for cabeza, cuerpos in gramatica.producciones.items():
        if CUERPO_VACIO in cuerpos:
            anulables.add(cabeza)
    if registrar:
        registrar(0, set(anulables), "producciones directas A -> ε")

    # --- Inducción: punto fijo ---
    iteracion = 1
    while True:
        nuevos = set()
        motivos = []
        for cabeza, cuerpos in gramatica.producciones.items():
            if cabeza in anulables:
                continue
            for cuerpo in cuerpos:
                if cuerpo and all(simbolo in anulables for simbolo in cuerpo):
                    nuevos.add(cabeza)
                    motivos.append(f"{cabeza} -> {''.join(cuerpo)}")
                    break
        if not nuevos:
            if registrar:
                registrar(iteracion, set(anulables), "sin cambios: se detiene")
            break
        anulables |= nuevos
        if registrar:
            registrar(iteracion, set(anulables), ", ".join(motivos))
        iteracion += 1

    return anulables


def combinaciones_de_cuerpo(cuerpo, anulables):
    """Genera las 2^m versiones de un cuerpo según sus m símbolos anulables.

    Devuelve una lista de tuplas (cuerpo_resultante, conservados) sin repetir,
    donde 'conservados' indica qué símbolos anulables se mantuvieron.
    """
    posiciones_anulables = [i for i, s in enumerate(cuerpo) if s in anulables]
    resultados = []
    vistos = set()

    # Cada símbolo anulable se conserva (True) o se elimina (False).
    for eleccion in product([True, False], repeat=len(posiciones_anulables)):
        decision = dict(zip(posiciones_anulables, eleccion))
        nuevo = tuple(
            s for i, s in enumerate(cuerpo) if decision.get(i, True)
        )
        if nuevo not in vistos:
            vistos.add(nuevo)
            resultados.append((nuevo, decision))

    return resultados


def eliminar_producciones_epsilon(gramatica, registrar=None, preservar_vacio=False):
    """Construye una gramática equivalente sin producciones-ε.

    Devuelve (nueva_gramatica, anulables, descartadas).
    """
    anulables = encontrar_anulables(gramatica)
    nueva = Gramatica(simbolo_inicial=gramatica.simbolo_inicial)
    descartadas = []

    for cabeza in gramatica.orden:
        for cuerpo in gramatica.producciones[cabeza]:
            if cuerpo == CUERPO_VACIO:
                descartadas.append((cabeza, cuerpo, "es una producción-ε"))
                continue

            combinaciones = combinaciones_de_cuerpo(cuerpo, anulables)
            if registrar:
                registrar(cabeza, cuerpo, combinaciones, anulables)

            for nuevo_cuerpo, _ in combinaciones:
                if nuevo_cuerpo == CUERPO_VACIO:
                    descartadas.append(
                        (cabeza, cuerpo, "la combinación vacía se descarta")
                    )
                    continue
                nueva.agregar(cabeza, nuevo_cuerpo)

    # Si el lenguaje original contenía la cadena vacía, se puede conservar
    # agregando un nuevo símbolo inicial S0 -> S | ε.
    if preservar_vacio and gramatica.simbolo_inicial in anulables:
        nuevo_inicial = "S0"
        nueva.agregar(nuevo_inicial, (gramatica.simbolo_inicial,))
        nueva.agregar(nuevo_inicial, CUERPO_VACIO)
        nueva.simbolo_inicial = nuevo_inicial
        nueva.orden.remove(nuevo_inicial)
        nueva.orden.insert(0, nuevo_inicial)

    return nueva, anulables, descartadas
