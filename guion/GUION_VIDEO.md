# Guion para el video (máximo 10 minutos)

Duración sugerida: **6 a 7 minutos**. Lenguaje sencillo, sin tecnicismos de más.
Lo que va en *cursiva* son indicaciones de qué hacer en pantalla, no hay que leerlo.

---

## 1. Presentación (20 segundos)

*Pantalla: el repositorio de GitHub abierto.*

> "Hola, soy Harry Méndez y este es el Laboratorio 7 del curso de Teoría de la
> Computación. El programa está hecho en Python y hace dos cosas: primero valida
> que las gramáticas estén bien escritas usando una expresión regular, y después
> elimina las producciones épsilon, que son las producciones que generan la
> cadena vacía."

---

## 2. Recorrido rápido del proyecto (50 segundos)

*Pantalla: el explorador de archivos o el editor con las carpetas abiertas.*

> "El proyecto está dividido así:
> - En la carpeta `gramaticas` están los archivos de texto con las gramáticas.
>   Cada línea es una producción y se pueden poner varias separadas por el
>   símbolo de OR.
> - En `src` está el código: `validador.py` tiene la expresión regular,
>   `gramatica.py` lee el archivo, `epsilon.py` tiene el algoritmo y `main.py`
>   muestra todo en pantalla paso por paso.
> - Y en `tests` están las pruebas unitarias."

*Abrir `gramaticas/gramatica1.txt` y mostrarlo.*

> "Esta es la primera gramática. Las mayúsculas son no terminales, las minúsculas
> y los números son terminales, y la épsilon representa la cadena vacía."

---

## 3. La validación con la expresión regular (1 minuto)

*Abrir `src/validador.py`.*

> "Aquí está la expresión regular. Lo que dice, en palabras simples, es:
> una letra mayúscula, después una flecha, y después uno o más cuerpos de
> producción separados por el símbolo de OR. Cada cuerpo puede ser una
> secuencia de letras y números, o puede ser épsilon.
> Si una línea no cumple con esto, el programa se detiene."

---

## 4. Demostración del error (1 minuto)  ⟵ *inciso obligatorio*

*Abrir `gramaticas/gramatica_con_error.txt` y mostrar que la línea 4 dice `A -> C |`.*

> "Voy a demostrar la validación. Fíjense en esta línea: dice A, flecha, C, y un
> OR que queda suelto, sin nada después. Eso está mal escrito."

*Ejecutar en la terminal:*

```bash
python lab7.py gramaticas/gramatica_con_error.txt
```

> "Y ahí está: el programa valida la línea 3 sin problema, pero al llegar a la
> línea 4 marca el error, dice exactamente cuál es la línea que está mal, y
> detiene la ejecución. No continúa con el algoritmo."

*Opcional: editar el archivo en vivo, poner otro error distinto —por ejemplo
cambiar la mayúscula por minúscula o quitar la flecha— guardar, y volver a
ejecutar para que se vea que también lo detecta.*

---

## 5. Ejecución de la gramática 1 (1 minuto y medio)

*Ejecutar:*

```bash
python lab7.py gramaticas/gramatica1.txt
```

> "Ahora sí, con la gramática correcta. En el paso 1 valida todas las líneas y
> todas pasan. En el paso 2 muestra la gramática que cargó, con su símbolo
> inicial, sus no terminales y sus terminales."

*Señalar el paso 3.*

> "El paso 3 es la parte interesante: busca los símbolos anulables, que son los
> que pueden llegar a producir la cadena vacía. Empieza con los que tienen una
> producción directa a épsilon —en este caso C— y luego va repitiendo: si un
> símbolo produce algo donde todo es anulable, entonces ese símbolo también es
> anulable. Repite hasta que ya no cambia nada. Al final todos resultan
> anulables: S, A, B y C."

*Señalar el paso 4.*

> "En el paso 4 genera las nuevas producciones. Para cada producción cuenta
> cuántos símbolos anulables tiene, y de ahí salen dos elevado a esa cantidad de
> casos. Por ejemplo aquí, S produce 0A0, y como A es anulable hay dos casos:
> dejarla, o quitarla, y queda 0-0."

*Señalar el paso 5.*

> "Y este es el resultado final: la gramática ya sin ninguna producción épsilon."

---

## 6. Ejecución de la gramática 2 (1 minuto y medio)

*Ejecutar:*

```bash
python lab7.py gramaticas/gramatica2.txt
```

> "Con la segunda gramática se ve mejor lo de las combinaciones. Aquí S produce
> A-B-a-C, y tres de esos símbolos son anulables: A, B y C. Entonces son dos
> elevado a la tres, ocho casos posibles, y el programa los muestra todos uno
> por uno diciendo qué símbolo quitó en cada caso."

*Señalar que la combinación que queda vacía se descarta.*

> "Cuando la combinación deja el cuerpo completamente vacío, se descarta, porque
> justamente lo que queremos es que ya no queden producciones épsilon."

---

## 7. Pruebas unitarias (40 segundos)

*Ejecutar:*

```bash
python -m unittest discover -s tests -v
```

> "Por último tengo pruebas unitarias que comprueban la expresión regular con
> casos válidos e inválidos, el conjunto de símbolos anulables, la cantidad de
> combinaciones, y que el resultado final sea el correcto para las dos
> gramáticas. Las trece pruebas pasan."

---

## 8. Cierre (15 segundos)

> "Eso sería todo. El código, las gramáticas y el documento con las respuestas
> están en el repositorio, y el enlace de este video está en el README.
> Muchas gracias."

---

## Lista de verificación antes de grabar

- [ ] Terminal con letra grande (para que se lea en el video).
- [ ] Terminal ubicada en la carpeta del proyecto.
- [ ] Limpiar la pantalla entre ejecuciones (`clear`).
- [ ] Tener abiertos: `gramatica1.txt`, `gramatica_con_error.txt` y `validador.py`.
- [ ] Probar el audio antes de empezar.
- [ ] Al terminar: subir a YouTube como **no listado** y pegar el enlace en el README.
