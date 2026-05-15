# Agujeros negros

@subtitle Un viaje a los objetos más extremos del universo


## Introducción

Un **agujero negro** es una región del espacio-tiempo donde la gravedad es tan intensa que ni siquiera la luz puede escapar.

Este concepto surge de la teoría de la *relatividad general* formulada por Albert Einstein.

Puedes leer más sobre esto en el artículo de [Relatividad general](relatividad.html).

@quote Esto es una cita.   - A. Einstein


@image test.jpg | zgz.jpg | Representación artística de un agujero negro | 200px


## Historia

### Primeras ideas

Ya en el siglo XVIII, John Michell propuso la existencia de “estrellas oscuras”, objetos tan masivos que la luz no podía escapar.

### Relatividad general

En 1915, Einstein desarrolló la teoría que explica la gravedad como curvatura del espacio-tiempo.


@note Importante: el concepto moderno de agujero negro no es simplemente una estrella apagada, sino una deformación extrema del espacio-tiempo.


## Fundamentos físicos

La gravedad depende de la masa y la distancia. Cuanto más concentrada está la masa, mayor es la curvatura.

La relación entre masa y energía viene dada por:

$$E = mc^2$$

El radio de Schwarzschild es:

$$r_s = \frac{2GM}{c^2}$$


## Simulación (ejemplo de código)

Podemos aproximar el radio de un agujero negro con este código:

```python
G = 6.67e-11
c = 3e8

def radio_schwarzschild(M):
    return (2 * G * M) / (c**2)

masa_sol = 1.989e30
print(radio_schwarzschild(masa_sol))