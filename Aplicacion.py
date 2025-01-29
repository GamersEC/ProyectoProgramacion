# Agrega esto AL PRINCIPIO de tu código (antes de cualquier import de matplotlib)
import matplotlib

matplotlib.use('QtAgg')

# Luego tus imports normales
import sys
from PyQt6 import QtWidgets, QtCore
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QFileDialog, QMessageBox,
    QStackedWidget, QDialog, QComboBox, QFormLayout, QScrollArea, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap


# Nueva clase para la ventana de login
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.setWindowIcon(QIcon("icons/login.png"))
        self.setGeometry(500, 250, 400, 350)

        # Cargar CSS externo
        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())

        layout = QVBoxLayout()

        # Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("icons/logo.png")
        self.logo_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Campos de entrada
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Usuario")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        # Botón de login
        self.login_button = QPushButton("Iniciar Sesión", self)
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")


class DataLoaderThread(QThread):
    loaded = pyqtSignal(pd.DataFrame)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            if self.file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.csv'):
                df = pd.read_csv(self.file_path)
            self.loaded.emit(df)
        except Exception as e:
            self.error.emit(str(e))


class AnalysisWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Análisis Detallado")
        self.setGeometry(400, 400, 800, 600)

        layout = QVBoxLayout()
        scroll = QScrollArea()
        content = QWidget()
        scroll_layout = QVBoxLayout(content)

        # Estadísticas descriptivas
        stats = data.describe().reset_index()
        self.add_table(scroll_layout, "Estadísticas Descriptivas", stats)

        # Tipos de datos
        dtype_df = pd.DataFrame(data.dtypes.reset_index())
        dtype_df.columns = ['Columna', 'Tipo de Dato']
        self.add_table(scroll_layout, "Tipos de Datos", dtype_df)

        # Valores faltantes
        missing_df = pd.DataFrame(data.isnull().sum()).reset_index()
        missing_df.columns = ['Columna', 'Valores Faltantes']
        self.add_table(scroll_layout, "Valores Faltantes", missing_df)

        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def add_table(self, layout, title, df):
        layout.addWidget(QLabel(f"<b>{title}</b>"))
        table = QTableWidget()
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        layout.addWidget(table)


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App de Análisis de Datos")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icons/analysis.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)

        # **Panel izquierdo más ancho y responsivo**
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        left_panel.setMinimumWidth(250)  # Ancho mínimo más grande
        left_panel.setMaximumWidth(400)  # Ancho máximo para evitar que crezca demasiado
        left_panel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        # **Botones más grandes**
        button_size = QtCore.QSize(220, 50)  # Tamaño uniforme para los botones

        self.load_button = QPushButton("Cargar Datos")
        self.load_button.setIcon(QIcon("icons/load.png"))
        self.load_button.setMinimumSize(button_size)

        self.analysis_button = QPushButton("Análisis Avanzado")
        self.analysis_button.setIcon(QIcon("icons/analysis.png"))
        self.analysis_button.setMinimumSize(button_size)

        self.graph_button = QPushButton("Generar Gráfica")
        self.graph_button.setIcon(QIcon("icons/graph.png"))
        self.graph_button.setMinimumSize(button_size)

        self.save_button = QPushButton("Guardar Datos")
        self.save_button.setIcon(QIcon("icons/save.png"))
        self.save_button.setMinimumSize(button_size)

        self.back_button = QPushButton("Volver a la tabla")
        self.back_button.setIcon(QIcon("icons/back.png"))
        self.back_button.setMinimumSize(button_size)
        self.back_button.setVisible(False)

        # **Alinear los botones al centro y distribuir espacio proporcionalmente**
        left_layout.addStretch()
        left_layout.addWidget(self.load_button, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.analysis_button, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.graph_button, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addStretch()

        # **Hacer que el contenido principal sea flexible**
        self.stacked_widget = QStackedWidget()
        self.table_widget = QTableWidget()
        self.graph_widget = GraphWidget()

        self.stacked_widget.addWidget(self.table_widget)
        self.stacked_widget.addWidget(self.graph_widget)

        # **Agregar los elementos al layout principal**
        main_layout.addWidget(left_panel, 2)  # Menú ocupa 2 partes
        main_layout.addWidget(self.stacked_widget, 5)  # Contenido ocupa 5 partes

        # **Conexiones**
        self.load_button.clicked.connect(self.load_data)
        self.analysis_button.clicked.connect(self.show_analysis)
        self.graph_button.clicked.connect(self.generate_graph)
        self.save_button.clicked.connect(self.save_data)
        self.back_button.clicked.connect(self.show_table)

        self.data = None



    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo", "",
            "Archivos de Datos (*.xlsx *.xls *.csv)"
        )

        if file_path:
            self.thread = DataLoaderThread(file_path)
            self.thread.loaded.connect(self.on_data_loaded)
            self.thread.error.connect(self.show_error)
            self.thread.start()

    def on_data_loaded(self, df):
        self.data = df
        self.populate_table()
        QMessageBox.information(self, "Éxito", f"Datos cargados: {len(df)} registros")

    def show_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"Error al cargar: {error_msg}")

    def populate_table(self, max_rows=1000):
        if self.data is not None:
            df = self.data.head(max_rows)
            self.table_widget.setRowCount(len(df))
            self.table_widget.setColumnCount(len(df.columns))
            self.table_widget.setHorizontalHeaderLabels(df.columns)

            for row_idx, row in df.iterrows():
                for col_idx, value in enumerate(row):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def show_analysis(self):
        if self.data is not None:
            self.analysis_window = AnalysisWindow(self.data, self)
            self.analysis_window.exec()
        else:
            QMessageBox.warning(self, "Advertencia", "No hay datos cargados")

    def generate_graph(self):
        if self.data is not None:
            try:
                self.graph_widget.figure.clear()
                ax = self.graph_widget.figure.add_subplot(111)

                # Seleccionar solo columnas numéricas
                numeric_data = self.data.select_dtypes(include=[np.number])
                if numeric_data.empty:
                    raise ValueError("No hay columnas numéricas para graficar")

                numeric_data.plot(ax=ax)
                ax.set_title("Gráfico de datos numéricos")
                self.graph_widget.canvas.draw()
                self.stacked_widget.setCurrentWidget(self.graph_widget)
                self.back_button.setVisible(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "No hay datos cargados")

    def show_table(self):
        self.stacked_widget.setCurrentWidget(self.table_widget)
        self.back_button.setVisible(False)

    def save_data(self):
        if self.data is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "",
                                                       "CSV Files (*.csv);;Excel Files (*.xlsx)")
            if file_path:
                if file_path.endswith(".csv"):
                    self.data.to_csv(file_path, index=False)
                elif file_path.endswith(".xlsx"):
                    self.data.to_excel(file_path, index=False)
                QMessageBox.information(self, "Éxito", "Datos guardados correctamente")
        else:
            QMessageBox.warning(self, "Error", "No hay datos para guardar")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Muestra la ventana de login
    login_window = LoginWindow()
    if login_window.exec() == QDialog.DialogCode.Accepted:
        # Si el login es exitoso, muestra la ventana principal
        window = DataAnalysisApp()
        window.show()
        sys.exit(app.exec())