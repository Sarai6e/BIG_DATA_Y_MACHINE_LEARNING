import numpy as np

# Ingresar 9 números y agregar 0 al final
matriz = np.array([int(input(f"Ingrese el número {i+1}: ")) for i in range(9)] + [0])

# Buscar la posición del número 0
for i, num in enumerate(matriz):
    if num == 0:
        print(f"El número 0 está en el orden {i+1}")
