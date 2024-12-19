import pandas as pd

# Función para leer el archivo .xlsx y extraer los datos en un DataFrame
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

# Función para contar las ocurrencias de una palabra en el DataFrame
def contar_palabras(df, palabra):
    conteo = 0
    for columna in df.columns:
        conteo += df[columna].astype(str).str.contains(palabra, case=False, na=False).sum()
    return conteo

# Función para reemplazar una palabra por otra en el DataFrame
def reemplazar_palabra(df, palabra_antigua, palabra_nueva):
    for columna in df.columns:
        df[columna] = df[columna].astype(str).replace(palabra_antigua, palabra_nueva, regex=True)
    return df

# Función para identificar columnas numéricas
def obtener_columnas_numericas(df):
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    return columnas_numericas

# Función para sumar los valores de una columna seleccionada
def sumar_columna(df, columna):
    return df[columna].sum()

# Función para añadir datos al DataFrame
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

        confirmacion = input("\n¿Quieres guardar estos datos? (s/n/no estoy seguro): ").lower()
        if confirmacion == 's':
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            print("Datos guardados.")
        elif confirmacion == 'n':
            print("Datos descartados.")
        elif confirmacion == "no estoy seguro":
            print("Volviendo a llenar datos...")
            continue

        continuar = input("\n¿Quieres añadir otra fila? (s/n): ").lower()
        if continuar != 's':
            break

    return df

# Función para guardar el contenido modificado en un archivo
def guardar_archivo(df, nombre_archivo):
    try:
        df.to_excel(nombre_archivo, index=False)
        print(f"Archivo guardado como '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Función principal
def main():
    nombre_archivo_entrada = input("Introduce el nombre del archivo XLSX (con extensión .xlsx): ")

    # Verificar si el archivo tiene la extensión correcta
    if not nombre_archivo_entrada.endswith(".xlsx"):
        print("El archivo debe tener la extensión .xlsx")
        return

    # Leer el archivo
    df = leer_archivo(nombre_archivo_entrada)
    if df is None:
        return

    print("\nContenido del archivo:")
    print(df)

    # Preguntar qué palabra buscar
    palabra_buscar = input("\n¿Qué palabra deseas buscar? ")

    # Contar las ocurrencias de la palabra
    ocurrencias = contar_palabras(df, palabra_buscar)
    print(f"La palabra '{palabra_buscar}' se encontró {ocurrencias} veces.")

    # Preguntar si se desea reemplazar la palabra
    reemplazar = input("\u00bfDeseas reemplazar esta palabra? (s/n): ")
    if reemplazar.lower() == 's':
        palabra_nueva = input(f"\u00bfPor qué palabra deseas reemplazar '{palabra_buscar}'? ")
        df = reemplazar_palabra(df, palabra_buscar, palabra_nueva)
        print("\nContenido después de reemplazar:")
        print(df)

    # Identificar columnas numéricas
    columnas_numericas = obtener_columnas_numericas(df)
    if not columnas_numericas:
        print("No se encontraron columnas numéricas en el archivo.")
    else:
        print("\nColumnas numéricas disponibles para sumar:")
        for i, columna in enumerate(columnas_numericas, 1):
            print(f"{i}. {columna}")

        # Preguntar al usuario cuál columna sumar
        try:
            opcion = int(input("Selecciona el número de la columna que deseas sumar: "))
            if 1 <= opcion <= len(columnas_numericas):
                columna_seleccionada = columnas_numericas[opcion - 1]
                suma = sumar_columna(df, columna_seleccionada)
                print(f"La suma de los valores en la columna '{columna_seleccionada}' es: {suma}")
            else:
                print("Opción inválida. No se realizará ninguna suma.")
        except ValueError:
            print("Entrada inválida. No se realizará ninguna suma.")

    # Preguntar si desea añadir más datos
    anadir = input("\n¿Deseas añadir más datos al archivo? (s/n): ")
    if anadir.lower() == 's':
        df = anadir_datos(df)

    # Guardar el contenido modificado en un nuevo archivo
    nombre_archivo_salida = "resultado_modificado.xlsx"
    guardar_archivo(df, nombre_archivo_salida)
    print(f"\nProceso completado. El archivo modificado ha sido guardado como '{nombre_archivo_salida}'.")

if __name__ == "__main__":
    main()