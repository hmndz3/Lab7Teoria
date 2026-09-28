# Laboratorio 7 — Teoría de la Computación

Harry Méndez

## Respuestas del Ejercicio No. 2

📄 **[Lab7_Ejercicio2.pdf](documentos/Lab7_Ejercicio2.pdf)** — los ejercicios resueltos a mano.

## Video de demostración

🎥 **[Ver video en YouTube](PEGAR_AQUI_EL_ENLACE)**

---

## De qué trata

Este programa toma una gramática libre de contexto escrita en un archivo de
texto, revisa que esté bien escrita y le quita las producciones-ε, que son las
producciones que generan la cadena vacía. El resultado es una gramática
equivalente, pero sin ese tipo de producciones.

Está hecho en **Python 3** y no necesita instalar nada.

## Cómo se usa

```bash
python lab7.py gramaticas/gramatica1.txt
python lab7.py gramaticas/gramatica2.txt
python lab7.py gramaticas/gramatica3.txt
```

Para ver qué pasa cuando una gramática está mal escrita:

```bash
python lab7.py gramaticas/gramatica_con_error.txt
```

Y para correr las pruebas:

```bash
python -m unittest discover -s tests -v
```

## Cómo se escriben las gramáticas

Cada línea del archivo es una producción. Si hay varias opciones, se separan
con una barra vertical `|`.

```
S -> aAa | bBb | ε
A -> C | a
```

- Las **mayúsculas** son no terminales.
- Las **minúsculas y los dígitos** son terminales.
- La **ε** es la cadena vacía.
- Las líneas que empiezan con `#` son comentarios y se ignoran.

## Qué hace el programa, paso a paso

**1. Revisa que cada línea esté bien escrita.** Usa una expresión regular que
pide: una letra mayúscula, una flecha, y uno o más cuerpos separados por `|`.
Si alguna línea no cumple, el programa dice qué línea está mal y **se detiene**
ahí mismo.

**2. Busca los símbolos anulables**, o sea los que pueden terminar produciendo
la cadena vacía. Empieza por los que tienen una producción directa a ε, y luego
va agregando los que producen algo formado solo por símbolos que ya son
anulables. Repite hasta que el conjunto deja de cambiar.

**3. Genera las nuevas producciones.** Si una producción tiene `m` símbolos
anulables, hay `2^m` formas de armarla: cada símbolo anulable se puede dejar o
quitar. El programa las muestra todas y descarta las que quedan vacías.

**4. Muestra la gramática final**, ya sin producciones-ε.

Si aparecen producciones unarias (como `S -> S` en la gramática 3), se dejan
tal cual: quitarlas es un paso aparte de la simplificación.

## Resultados

**Gramática 1**

```
S -> 0A0 | 1B1 | BB          S -> 0A0 | 00 | 1B1 | 11 | BB | B
A -> C                 ==>   A -> C
B -> S | A                   B -> S | A
C -> S | ε                   C -> S
```

**Gramática 2**

```
S -> aAa | bBb | ε           S -> aAa | aa | bBb | bb
A -> C | a                   A -> C | a
B -> C | b             ==>   B -> C | b
C -> CDE | ε                 C -> CDE | CE | DE | E
D -> A | B | ab              D -> A | B | ab
```

**Gramática 3**

```
S -> ASA | aB                S -> ASA | AS | SA | S | aB | a
A -> B | S             ==>   A -> B | S
B -> b | ε                   B -> b
```

## Archivos del repositorio

```
lab7.py          el programa (esto es lo que se ejecuta)
src/             el código: validación, lectura del archivo y el algoritmo
gramaticas/      las tres gramáticas del Ejercicio 2 y una con un error a propósito
tests/           15 pruebas unitarias
documentos/      el PDF con las respuestas
guion/           el guion usado para grabar el video
```
