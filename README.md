# Laboratorio 7 - Teoría de la Computación

Simplificación de gramáticas libres de contexto: **validación de producciones
con expresiones regulares** y **eliminación de producciones-ε**.

Lenguaje utilizado: **Python 3** (sin librerías externas).

## Video de demostración

📹 **[Ver video en YouTube](PEGAR_AQUI_EL_ENLACE)**

## Cómo ejecutar

```bash
python lab7.py gramaticas/gramatica1.txt
python lab7.py gramaticas/gramatica2.txt
```

Para demostrar la validación con una gramática mal escrita:

```bash
python lab7.py gramaticas/gramatica_con_error.txt
```

Opción extra: si el lenguaje original contenía la cadena vacía, se puede
conservar agregando un nuevo símbolo inicial `S0 -> S | ε`:

```bash
python lab7.py gramaticas/gramatica1.txt --preservar-vacio
```

Pruebas unitarias:

```bash
python -m unittest discover -s tests -v
```

## Estructura del repositorio

```
Lab7Teoria/
├── lab7.py                 # punto de entrada del programa
├── src/
│   ├── validador.py        # expresión regular que valida las producciones
│   ├── gramatica.py        # lectura del archivo y representación de la gramática
│   ├── epsilon.py          # símbolos anulables y eliminación de producciones-ε
│   └── main.py             # ejecución paso a paso en pantalla
├── gramaticas/
│   ├── gramatica1.txt      # gramática 1 del Ejercicio No. 2
│   ├── gramatica2.txt      # gramática 2 del Ejercicio No. 2
│   └── gramatica_con_error.txt   # caso inválido usado en el video
├── tests/test_lab7.py      # pruebas unitarias
├── documentos/             # respuestas en PDF de los incisos sin código
└── guion/GUION_VIDEO.md    # guion de la grabación
```

## Formato de los archivos de gramática

- Cada línea es una producción; puede tener varios cuerpos separados por `|`.
- Una letra **MAYÚSCULA** individual es un **no terminal**.
- Una letra **minúscula** o un **dígito** es un **terminal**.
- La cadena vacía se escribe `ε` (también se acepta `epsilon` o `&`).
- La flecha se escribe `->` o `→`.
- Las líneas en blanco y las que empiezan con `#` se ignoran.

Ejemplo:

```
S -> 0A0 | 1B1 | BB
A -> C
B -> S | A
C -> S | ε
```

## Expresión regular utilizada

```python
SIMBOLO = r"[A-Za-z0-9]"
VACIO   = r"(?:ε|epsilon|&)"
CUERPO  = rf"(?:{VACIO}|{SIMBOLO}+)"
FLECHA  = r"(?:->|→)"

PATRON_PRODUCCION = rf"^\s*[A-Z]\s*{FLECHA}\s*{CUERPO}(?:\s*\|\s*{CUERPO})*\s*$"
```

Lee así: una **mayúscula**, una **flecha**, y luego **uno o más cuerpos**
separados por el operador OR `|`, donde cada cuerpo es una secuencia de
símbolos o la cadena vacía. Si una línea no calza con el patrón, el programa
imprime el número de línea, el contenido del error y **detiene la ejecución**.

## Algoritmo de eliminación de producciones-ε

**Paso 1 — Encontrar los símbolos anulables** (punto fijo):

- *Base:* `A` es anulable si existe la producción `A -> ε`.
- *Inducción:* `A` es anulable si existe `A -> X1 X2 ... Xk` y **todos** los
  `Xi` ya son anulables.
- Se repite hasta que el conjunto ya no cambia.

**Paso 2 — Generar las nuevas producciones:** para cada producción
`A -> X1 ... Xk` con `m` símbolos anulables se construyen las **2^m**
combinaciones posibles (cada símbolo anulable se conserva o se elimina).
Se descartan los cuerpos que quedan vacíos, las producciones `A -> ε` y las
combinaciones inútiles del tipo `A -> A`.

## Resultados

### Gramática 1

| Original | Anulables | Sin producciones-ε |
|---|---|---|
| `S -> 0A0 \| 1B1 \| BB`<br>`A -> C`<br>`B -> S \| A`<br>`C -> S \| ε` | `{S, A, B, C}` | `S -> 0A0 \| 00 \| 1B1 \| 11 \| BB \| B`<br>`A -> C`<br>`B -> S \| A`<br>`C -> S` |

### Gramática 2

| Original | Anulables | Sin producciones-ε |
|---|---|---|
| `S -> ABaC`<br>`A -> BC`<br>`B -> b \| ε`<br>`C -> D \| ε`<br>`D -> d` | `{A, B, C}` | `S -> ABaC \| ABa \| AaC \| Aa \| BaC \| Ba \| aC \| a`<br>`A -> BC \| B \| C`<br>`B -> b`<br>`C -> D`<br>`D -> d` |
