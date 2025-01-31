import pandas as pd
import numpy as np

# Generar datos aleatorios
np.random.seed(42)  # Para reproducibilidad

n = 400  # Número de registros

nombres = ["Juan", "María", "Luis", "Ana", "Carlos", "Laura", "Pedro", "Sofía", "Jorge", "Mónica",
           "Fernando", "Gabriela", "Ricardo", "Isabel", "Héctor", "Adriana", "Oscar", "Patricia",
           "Francisco", "Claudia", "Roberto", "Verónica", "Enrique", "Diana", "José", "Teresa",
           "Manuel", "Lucía", "Raúl", "Silvia"]

apellidos = ["Pérez", "González", "Martínez", "Rodríguez", "Sánchez", "Díaz", "Gómez", "Ruiz", "Herrera",
             "Castro", "Vargas", "Mendoza", "Ríos", "Torres", "Núñez", "Silva", "Domínguez", "Luna",
             "Mora", "Rojas", "Campos", "Soto", "Guerrero", "Mejía", "León", "Medina", "Cortés",
             "Jiménez", "Espinoza", "Ochoa"]

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