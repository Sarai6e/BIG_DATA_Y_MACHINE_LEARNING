def bubble_sort(lista):
    for i in range(len(lista)):
      for j in range(len(lista)-i-1):
        if lista[j] > lista[j+1]:
            lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista
print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))

