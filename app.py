import pandas as pd
import os

def leer_archivo(nombre_archivo):
    try:
        df = pd.read_excel(nombre_archivo)
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encuentra.")
        return None
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        return None
    return df

def contar_palabras(df, palabra):
    conteo = 0
    for columna in df.columns:
        conteo += df[columna].astype(str).str.contains(palabra, case=False, na=False).sum()
    return conteo

def reemplazar_palabra(df, palabra_antigua, palabra_nueva):
    for columna in df.columns:
        df[columna] = df[columna].astype(str).replace(palabra_antigua, palabra_nueva, regex=True)
    return df

def obtener_columnas_numericas(df):
    # Identificar columnas numéricas sin modificar los datos
    columnas_numericas = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    return columnas_numericas

def sumar_columna(df, columna):
    return df[columna].sum()

def anadir_datos(df):
    while True:
        print("\nIntroduce los datos para las siguientes columnas:")
        nueva_fila = {}
        for columna in df.columns:
            valor = input(f"{columna}: ")
            nueva_fila[columna] = valor

        print("\nDatos ingresados:")
        for columna, valor in nueva_fila.items():
            print(f"{columna}: {valor}")

        confirmacion = input("\n¿Quieres guardar estos datos? (s/n): ").lower()
        if confirmacion == 's':
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            print("Datos guardados.")
        elif confirmacion == 'n':
            print("Datos descartados.")
            continue

        continuar = input("\n¿Quieres añadir otra fila? (s/n): ").lower()
        if continuar != 's':
            break

    return df

def guardar_archivo(df, nombre_archivo):
    try:
        if os.path.exists(nombre_archivo):
            # Leer el archivo existente
            df_existente = pd.read_excel(nombre_archivo)
            # Concatenar los datos existentes con los nuevos
            df = pd.concat([df_existente, df], ignore_index=True)
        # Guardar el DataFrame combinado
        df.to_excel(nombre_archivo, index=False)
        print(f"Archivo guardado como '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

def main():
    nombre_archivo_entrada = input("Introduce el nombre del archivo XLSX (nombre.xlsx): ")

    if not nombre_archivo_entrada.endswith(".xlsx"):
        print("El archivo debe tener la extensión .xlsx")
        return

    df = leer_archivo(nombre_archivo_entrada)
    if df is None:
        return

    print("\nContenido del archivo:")
    print(df)

    palabra_buscar = input("\n¿Qué palabra deseas buscar? ")
    ocurrencias = contar_palabras(df, palabra_buscar)
    print(f"La palabra '{palabra_buscar}' se encontró {ocurrencias} veces.")

    reemplazar = input("\u00bfDeseas reemplazar esta palabra? (s/n): ")
    if reemplazar.lower() == 's':
        palabra_nueva = input(f"\u00bfPor qué palabra deseas reemplazar '{palabra_buscar}'? ")
        df = reemplazar_palabra(df, palabra_buscar, palabra_nueva)
        print("\nContenido después de reemplazar:")
        print(df)

    columnas_numericas = obtener_columnas_numericas(df)
    if not columnas_numericas:
        print("No se encontraron columnas numéricas en el archivo.")
    else:
        print("\nSuma de valores por columna numérica:")
        for columna in columnas_numericas:
            suma = sumar_columna(df, columna)
            print(f"Total {columna}: {suma}")

    anadir = input("\n¿Deseas añadir más datos al archivo? (s/n): ")
    if anadir.lower() == 's':
        df = anadir_datos(df)

    nombre_archivo_salida = "resultado_modificado.xlsx"
    guardar_archivo(df, nombre_archivo_salida)
    print(f"\nProceso completado. El archivo modificado ha sido guardado como '{nombre_archivo_salida}'.")

if __name__ == "__main__":
    main()