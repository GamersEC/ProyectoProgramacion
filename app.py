import pandas as pd


# Función para leer el archivo .xlsx y extraer los datos en un DataFrame
def leer_archivo(nombre_archivo):
    try:
        df = pd.read_excel(nombre_archivo)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        return None
    return df


# Función para contar las ocurrencias de una palabra en el DataFrame
def contar_palabras(df, palabra):
    conteo = 0
    for columna in df.columns:
        conteo += df[columna].astype(str).str.contains(palabra, case=False).sum()
    return conteo


# Función para reemplazar una palabra por otra en el DataFrame
def reemplazar_palabra(df, palabra_antigua, palabra_nueva):
    for columna in df.columns:
        df[columna] = df[columna].astype(str).replace(palabra_antigua, palabra_nueva, regex=True)
    return df


# Función para extraer los números de un DataFrame y convertirlos a tipo float
def extraer_numeros(df):
    numeros = []
    for columna in df.columns:
        for valor in df[columna]:
            try:
                numeros.append(float(valor))
            except ValueError:
                pass  # Ignorar valores no numéricos
    return numeros


# Función para realizar una operación aritmética (por ejemplo, suma)
def realizar_operacion(numeros):
    if not numeros:
        print("No se encontraron números en el archivo.")
        return 0.0
    return sum(numeros)


# Función para guardar el contenido modificado en un archivo
def guardar_archivo(df, nombre_archivo):
    df.to_excel(nombre_archivo, index=False)


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
    reemplazar = input("¿Deseas reemplazar esta palabra? (s/n): ")
    if reemplazar.lower() == 's':
        palabra_nueva = input(f"¿Por qué palabra deseas reemplazar '{palabra_buscar}'? ")
        df = reemplazar_palabra(df, palabra_buscar, palabra_nueva)
        print("\nContenido después de reemplazar:")
        print(df)

    # Extraer los números y realizar una suma
    numeros = extraer_numeros(df)
    suma = realizar_operacion(numeros)
    print(f"La suma de los números es: {suma}")

    # Guardar el contenido modificado en un nuevo archivo
    nombre_archivo_salida = "resultado_modificado.xlsx"
    guardar_archivo(df, nombre_archivo_salida)
    print(f"\nProceso completado. El archivo modificado ha sido guardado como '{nombre_archivo_salida}'.")


if __name__ == "__main__":
    main()
