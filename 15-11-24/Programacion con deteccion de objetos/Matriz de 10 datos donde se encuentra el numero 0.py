import numpy as np

matriz = np.array([int(input(f"Ingrese el número {i+1}: ")) for i in range(10)])
for i, num in enumerate(matriz):
    if num == 0: print(f"El número 0 está en el orden {i+1}, posición {i}")
