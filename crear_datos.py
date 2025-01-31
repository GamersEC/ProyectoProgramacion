import pandas as pd
import numpy as np

# Generar datos aleatorios
np.random.seed(42)  # Para reproducibilidad

n = 400  # Número de registros

nombres = ["Juan Pérez", "María González", "Luis Martínez", "Ana Rodríguez", "Carlos Sánchez", "Laura Díaz",
           "Pedro Gómez", "Sofía Ruiz", "Jorge Herrera", "Mónica Castro", "Fernando Vargas", "Gabriela Mendoza",
           "Ricardo Ríos", "Isabel Torres", "Héctor Núñez", "Adriana Silva", "Oscar Domínguez", "Patricia Luna",
           "Francisco Mora", "Claudia Rojas", "Roberto Campos", "Verónica Soto", "Enrique Guerrero", "Diana Mejía",
           "José León", "Teresa Medina", "Manuel Cortés", "Lucía Jiménez", "Raúl Espinoza", "Silvia Ochoa"]

sexos = ["Masculino", "Femenino"]

# Crear DataFrame con datos médicos
data = {
    'Nombre': np.random.choice(nombres, n, replace=True),
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