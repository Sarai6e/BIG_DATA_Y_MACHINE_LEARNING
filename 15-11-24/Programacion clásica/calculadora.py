# Calculadora simple
a = float(input("Ingrese el primer número: "))
b = float(input("Ingrese el segundo número: "))
op = input("Ingrese la operación (+, -, *, /): ")

if op == '+':
    print("Resultado:", a + b)
elif op == '-':
    print("Resultado:", a - b)
elif op == '*':
    print("Resultado:", a * b)
elif op == '/':
    print("Resultado:", a / b if b != 0 else "Error: No se puede dividir entre cero.")
else:
    print("Operación no válida.")
