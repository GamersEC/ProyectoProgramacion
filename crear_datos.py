import pandas as pd
import numpy as np

data = {
    'ID': range(1, 101),
    'Edad': np.random.randint(18, 65, 100),
    'Salario': np.round(np.random.normal(35000, 7500, 100), 2),
    'Puntuacion': np.random.uniform(1.0, 10.0, 100),
    'Ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 100),
    'Fecha_Contrato': pd.date_range('2022-01-01', periods=100, freq='D'),
    'Activo': np.random.choice([True, False], 100)
}

df = pd.DataFrame(data)
df.to_excel('datos_ejemplo.xlsx', index=False)