import numpy as np

# Ingresar 10 números y convertirlos en una matriz
matriz = np.array([int(input(f"Ingrese el número {i+1}: ")) for i in range(10)])

# Mostrar la matriz
print("Matriz:", matriz)

# Mostrar las posiciones de los ceros
for i, num in enumerate(matriz):
    if num == 0:
        print(f"El número 0 se encuentra en el orden de ingreso {i+1} (posición en la matriz {i})")
