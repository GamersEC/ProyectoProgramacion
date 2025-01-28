import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Funciones del código base
def leer_archivo(nombre_archivo):
    try:
        df = pd.read_excel(nombre_archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no se encuentra.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir el archivo: {e}")
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
    return [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]

def sumar_columna(df, columna):
    return df[columna].sum()

def guardar_archivo(df, nombre_archivo):
    try:
        if os.path.exists(nombre_archivo):
            df_existente = pd.read_excel(nombre_archivo)
            df = pd.concat([df_existente, df], ignore_index=True)
        df.to_excel(nombre_archivo, index=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el archivo: {e}")
        return False

# Clase de la interfaz gráfica
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Archivos Excel")
        self.df = None
        self.archivo = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Marco principal para organizar mejor los elementos
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Botones y controles
        tk.Button(main_frame, text="Cargar Archivo Excel", command=self.cargar_archivo).grid(row=0, column=0, pady=5, sticky="ew")

        # Sección de búsqueda
        tk.Label(main_frame, text="Buscar palabra:").grid(row=1, column=0, sticky="w")
        self.palabra_buscar = tk.Entry(main_frame)
        self.palabra_buscar.grid(row=2, column=0, sticky="ew")
        tk.Button(main_frame, text="Contar Palabra", command=self.contar_palabra).grid(row=3, column=0, pady=5, sticky="ew")

        # Sección de reemplazo
        tk.Label(main_frame, text="Reemplazar palabra:").grid(row=4, column=0, sticky="w")
        self.palabra_reemplazar = tk.Entry(main_frame)
        self.palabra_reemplazar.grid(row=5, column=0, sticky="ew")
        tk.Label(main_frame, text="Por:").grid(row=6, column=0, sticky="w")
        self.palabra_nueva = tk.Entry(main_frame)
        self.palabra_nueva.grid(row=7, column=0, sticky="ew")
        tk.Button(main_frame, text="Reemplazar Palabra", command=self.reemplazar_palabra).grid(row=8, column=0, pady=5, sticky="ew")

        # Sección numérica
        tk.Button(main_frame, text="Mostrar Columnas Numéricas", command=self.mostrar_columnas_numericas).grid(row=9, column=0, pady=5, sticky="ew")
        tk.Label(main_frame, text="Columna a sumar:").grid(row=10, column=0, sticky="w")
        self.columna_sumar = tk.Entry(main_frame)
        self.columna_sumar.grid(row=11, column=0, sticky="ew")
        tk.Button(main_frame, text="Sumar Columna", command=self.sumar_columna).grid(row=12, column=0, pady=5, sticky="ew")

        # Sección de datos y guardado
        tk.Button(main_frame, text="Añadir Nuevos Datos", command=self.añadir_datos).grid(row=13, column=0, pady=5, sticky="ew")
        tk.Button(main_frame, text="Guardar Archivo Modificado", command=self.guardar_archivo).grid(row=14, column=0, pady=5, sticky="ew")

    def cargar_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if self.archivo:
            self.df = leer_archivo(self.archivo)
            if self.df is not None:
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")

    def contar_palabra(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        palabra = self.palabra_buscar.get()
        if not palabra:
            messagebox.showwarning("Advertencia", "Ingresa una palabra para buscar.")
            return
        conteo = contar_palabras(self.df, palabra)
        messagebox.showinfo("Resultado", f"La palabra '{palabra}' se encontró {conteo} veces.")

    def reemplazar_palabra(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        palabra_antigua = self.palabra_reemplazar.get()
        palabra_nueva = self.palabra_nueva.get()
        if not palabra_antigua or not palabra_nueva:
            messagebox.showwarning("Advertencia", "Ambos campos deben estar completos.")
            return
        self.df = reemplazar_palabra(self.df, palabra_antigua, palabra_nueva)
        messagebox.showinfo("Éxito", f"Se reemplazó '{palabra_antigua}' por '{palabra_nueva}'.")

    def mostrar_columnas_numericas(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        columnas = obtener_columnas_numericas(self.df)
        if columnas:
            messagebox.showinfo("Columnas Numéricas", "\n".join(columnas))
        else:
            messagebox.showinfo("Columnas Numéricas", "No se encontraron columnas numéricas.")

    def sumar_columna(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        columna = self.columna_sumar.get()
        if not columna:
            messagebox.showwarning("Advertencia", "Ingresa el nombre de una columna.")
            return
        if columna in self.df.columns:
            try:
                suma = sumar_columna(self.df, columna)
                messagebox.showinfo("Resultado", f"Suma de {columna}: {suma}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al sumar: {str(e)}")
        else:
            messagebox.showerror("Error", f"Columna '{columna}' no encontrada")

    def añadir_datos(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return

        nueva_fila = {}
        for columna in self.df.columns:
            valor = simpledialog.askstring("Añadir Datos", f"Valor para '{columna}':")
            if valor is None:  # Usuario canceló
                return
            nueva_fila[columna] = valor

        try:
            self.df = pd.concat([self.df, pd.DataFrame([nueva_fila])], ignore_index=True)
            messagebox.showinfo("Éxito", "Datos añadidos correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al añadir datos: {str(e)}")

    def guardar_archivo(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        archivo_salida = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        if archivo_salida:
            if guardar_archivo(self.df, archivo_salida):
                messagebox.showinfo("Éxito", f"Archivo guardado en:\n{archivo_salida}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()