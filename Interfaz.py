import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Archivos Excel")
        self.df = None
        self.archivo = None

        # Crear la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Botón para cargar archivo
        tk.Button(self.root, text="Cargar Archivo Excel", command=self.cargar_archivo).pack(pady=10)

        # Campo para buscar palabra
        tk.Label(self.root, text="Buscar palabra:").pack()
        self.palabra_buscar = tk.Entry(self.root)
        self.palabra_buscar.pack(pady=5)
        tk.Button(self.root, text="Contar Palabra", command=self.contar_palabra).pack()

        # Campo para reemplazar palabra
        tk.Label(self.root, text="Reemplazar palabra:").pack()
        self.palabra_reemplazar = tk.Entry(self.root)
        tk.Label(self.root, text="Por:").pack()
        self.palabra_nueva = tk.Entry(self.root)
        self.palabra_nueva.pack(pady=5)
        tk.Button(self.root, text="Reemplazar Palabra", command=self.reemplazar_palabra).pack()

        # Botón para mostrar columnas numéricas
        tk.Button(self.root, text="Mostrar Columnas Numéricas", command=self.mostrar_columnas_numericas).pack(pady=10)

        # Campo para sumar columna
        tk.Label(self.root, text="Seleccionar columna para sumar:").pack()
        self.columna_sumar = tk.Entry(self.root)
        self.columna_sumar.pack(pady=5)
        tk.Button(self.root, text="Sumar Columna", command=self.sumar_columna).pack()

        # Botón para añadir nuevos datos
        tk.Button(self.root, text="Añadir Nuevos Datos", command=self.añadir_datos).pack(pady=10)

        # Botón para guardar archivo
        tk.Button(self.root, text="Guardar Archivo Modificado", command=self.guardar_archivo).pack(pady=10)

    def cargar_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if self.archivo:
            try:
                self.df = pd.read_excel(self.archivo)
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo.\n{e}")

    def contar_palabra(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        palabra = self.palabra_buscar.get()
        conteo = self.df.astype(str).apply(lambda col: col.str.contains(palabra, case=False, na=False)).sum().sum()
        messagebox.showinfo("Resultado", f"La palabra '{palabra}' se encontró {conteo} veces.")

    def reemplazar_palabra(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        palabra_antigua = self.palabra_reemplazar.get()
        palabra_nueva = self.palabra_nueva.get()
        self.df.replace(palabra_antigua, palabra_nueva, regex=True, inplace=True)
        messagebox.showinfo("Éxito", f"Se reemplazó '{palabra_antigua}' por '{palabra_nueva}'.")

    def mostrar_columnas_numericas(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        columnas = [col for col in self.df.columns if pd.api.types.is_numeric_dtype(self.df[col])]
        if columnas:
            messagebox.showinfo("Columnas Numéricas", "\n".join(columnas))
        else:
            messagebox.showinfo("Columnas Numéricas", "No se encontraron columnas numéricas.")

    def sumar_columna(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        columna = self.columna_sumar.get()
        if columna in self.df.columns:
            try:
                suma = self.df[columna].sum()
                messagebox.showinfo("Resultado", f"La suma de la columna '{columna}' es: {suma}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo realizar la suma.\n{e}")
        else:
            messagebox.showerror("Error", f"La columna '{columna}' no existe.")

    def añadir_datos(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return

        nuevas_filas = []
        for columna in self.df.columns:
            valor = tk.simpledialog.askstring("Añadir Datos", f"Ingrese el valor para '{columna}':")
            if valor is None:
                return
            nuevas_filas.append(valor)

        nueva_fila = pd.DataFrame([dict(zip(self.df.columns, nuevas_filas))])
        self.df = pd.concat([self.df, nueva_fila], ignore_index=True)
        messagebox.showinfo("Éxito", "Datos añadidos correctamente.")

    def guardar_archivo(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero carga un archivo.")
            return
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if archivo_salida:
            self.df.to_excel(archivo_salida, index=False)
            messagebox.showinfo("Éxito", f"Archivo guardado como '{archivo_salida}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
