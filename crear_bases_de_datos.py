import pandas as pd
import numpy as np

# Preguntar al usuario cuántos registros quiere generar
n = int(input("Ingrese el número de registros a generar: "))

# Generar datos aleatorios
np.random.seed(42)  # Para reproducibilidad

nombres = ["Juan", "María", "Luis", "Ana", "Carlos", "Laura", "Pedro", "Sofía", "Jorge", "Mónica",
           "Fernando", "Gabriela", "Ricardo", "Isabel", "Héctor", "Adriana", "Oscar", "Patricia",
           "Francisco", "Claudia", "Roberto", "Verónica", "Enrique", "Diana", "José", "Teresa",
           "Manuel", "Lucía", "Raúl", "Silvia", "Eduardo", "Beatriz", "Andrés", "Elena", "Fabián",
           "Natalia", "Sebastián", "Rosa", "Hugo", "Camila", "David", "Antonella", "Cristian",
           "Valentina", "Esteban", "Margarita", "Diego", "Florencia", "Guillermo", "Regina",
           "Santiago", "Miranda", "Daniel", "Ariadna", "Martín", "Emilia", "Alberto", "Paula",
           "Álvaro", "Renata", "Agustín", "Lourdes", "Joaquín", "Fátima", "Felipe", "Cecilia",
           "Iván", "Alejandra", "Bruno", "Fernanda", "Tomás", "Ximena", "Emiliano", "Carolina",
           "Ramiro", "Jimena", "Luciano", "Estefanía", "Maximiliano", "Liliana"]

apellidos = ["Pérez", "González", "Martínez", "Rodríguez", "Sánchez", "Díaz", "Gómez", "Ruiz", "Herrera",
             "Castro", "Vargas", "Mendoza", "Ríos", "Torres", "Núñez", "Silva", "Domínguez", "Luna",
             "Mora", "Rojas", "Campos", "Soto", "Guerrero", "Mejía", "León", "Medina", "Cortés",
             "Jiménez", "Espinoza", "Ochoa", "Ortega", "Delgado", "Navarro", "Salazar", "Fuentes",
             "Valenzuela", "Paredes", "Cabrera", "Aguirre", "Miranda", "Escobar", "Avendaño",
             "Montoya", "Solís", "Ponce", "Peña", "Cárdenas", "Bravo", "Esquivel", "Coronado",
             "Castañeda", "Palacios", "Rentería", "Santana", "Galindo", "Olvera", "Rosales",
             "Trejo", "Hernández", "Peralta", "Zamora", "Pizarro", "Benítez", "Garrido", "Arenas",
             "Villarreal", "Salas", "Montero", "Maldonado", "Téllez", "Bermúdez", "Vallejo",
             "Quiroga", "Cardozo", "Ledesma", "Cuellar", "Sepúlveda", "Reynoso", "Gudiño"]

sexos = ["Masculino", "Femenino"]

# Crear DataFrame con datos médicos
data = {
    'Nombre': np.random.choice(nombres, n, replace=True),
    'Apellido': np.random.choice(apellidos, n, replace=True),
    'Edad': np.random.randint(18, 80, n),
    'Sexo': np.random.choice(sexos, n),
    'Saturación_Oxígeno': np.random.randint(88, 100, n),
    'Presión_Arterial': [f"{np.random.randint(100, 160)}/{np.random.randint(60, 100)}" for _ in range(n)],
    'Pulso': np.random.randint(60, 110, n),
    'Temperatura': np.round(np.random.uniform(36.0, 38.0, n), 1),
    'IMC': np.round(np.random.uniform(18.5, 35.0, n), 1)
}

df = pd.DataFrame(data)

# Guardar en un archivo Excel
df.to_excel('datos_medicos.xlsx', index=False)

# Mensaje de confirmación
print("¡Datos creados!")