# Operadores

print(3 + 4)
print(3 - 4)
print(3 * 4)
print(3 / 4)
print(10 % 3) #Mod
print(10 // 3) #Aproximar a un numero entero
print(2 ** 3) #Elevar un numero


print("Hola " + "Python " + "Qué tal ") #Lo mas comun usar el + en cadenas de texto
print("Hola " + str(5)) #Forzar el dato a string
print("Hola " * 5)

my_float = 2.5 * 2
print("Hola " * int(my_float)) #Convertimos a entero

## Operadores Comparativos

print(3 > 4)
print(3 < 4)
print(3 >= 4)
print(3 <= 4)
print(3 == 4)
print(3 != 4)

# Aqui se calcula o compara la ordenación alfabetica
# Con len podemos contar caracteres

print("Hola" > "Python")
print("Hola" < "Python")
print("Hola" >= "Aola")
print(len("Hola") >= len("Aoola"))
print("Hola" <= "Python")
print("Hola" == "Hola")
print("Hola" != "Python")

# Operadores lógicos

print(3 > 4 and "Hola" > "Python")
print(3 > 4 or "Hola" > "Python")
print(3 < 4 and "Hola" < "Python")
print(3 < 4 or "Hola" < "Python")
print(3 < 4 or ("Hola" > "Python" and 4 == 4))
print(not(3 > 4))