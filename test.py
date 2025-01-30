# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('QtAgg')

import sys
import seaborn as sns
import pandas as pd
import numpy as np
from PyQt6 import QtWidgets, QtCore
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QFileDialog, QMessageBox,
    QStackedWidget, QDialog, QComboBox, QFormLayout, QScrollArea, QLineEdit,
    QFrame, QSizePolicy, QTabWidget, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

sns.set_theme(style="darkgrid")

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App de Análisis de Datos")
        self.setWindowIcon(QIcon("icons/login.png"))
        self.setMinimumSize(400, 500)
        self.attempts = 0
        self.setup_ui()
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        if self.screen():
            cp = self.screen().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(25, 25, 25, 25)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap("icons/logo_login.png")
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap.scaled(
                180, 180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        title = QLabel("Iniciar Sesión")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("loginTitle")

        # Campos de entrada
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        form_layout = QFormLayout(input_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setVerticalSpacing(20)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFixedHeight(45)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(45)

        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Contraseña:", self.password_input)

        # Botón de login
        self.login_button = QPushButton("Ingresar al Sistema")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.check_credentials)

        # Pie de página
        footer = QLabel(
            "UNIVERSIDAD NACIONAL DE CHIMBORAZO\n"
            "Ingeniería en Ciencia de Datos e Inteligencia Artificial\n"
            "© 2024-2025"
        )
        footer.setObjectName("loginFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ensamblado final
        container_layout.addWidget(self.logo_label)
        container_layout.addWidget(title)
        container_layout.addWidget(input_frame)
        container_layout.addWidget(self.login_button)
        container_layout.addStretch()

        main_layout.addWidget(container)
        main_layout.addWidget(footer, alignment=Qt.AlignmentFlag.AlignBottom)

    def check_credentials(self):
        if self.attempts >= 3:
            QMessageBox.critical(self, "Bloqueado", "Demasiados intentos fallidos")
            self.reject()
            return

        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.accept()
        else:
            self.attempts += 1
            remaining = 3 - self.attempts
            QMessageBox.warning(
                self,
                "Error",
                f"Credenciales incorrectas\nIntentos restantes: {remaining}"
            )

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
            else:
                raise ValueError("Formato de archivo no soportado")
            self.loaded.emit(df)
        except Exception as e:
            self.error.emit(str(e))

class SearchReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Buscar y Reemplazar")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.search_input = QLineEdit()
        self.replace_input = QLineEdit()
        self.case_checkbox = QCheckBox("Coincidir mayúsculas/minúsculas")

        form_layout.addRow("Buscar:", self.search_input)
        form_layout.addRow("Reemplazar con:", self.replace_input)

        self.replace_btn = QPushButton("Reemplazar Todo")
        self.replace_btn.clicked.connect(self.accept)

        layout.addLayout(form_layout)
        layout.addWidget(self.case_checkbox)
        layout.addWidget(self.replace_btn)

class AddDataDialog(QDialog):
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Añadir Nuevo Registro")
        self.setFixedSize(450, 550)

        layout = QVBoxLayout(self)
        self.inputs = {}

        for col in self.columns:
            self.inputs[col] = QLineEdit()
            layout.addWidget(QLabel(col))
            layout.addWidget(self.inputs[col])

        self.add_btn = QPushButton("Añadir Registro")
        self.add_btn.clicked.connect(self.accept)
        layout.addWidget(self.add_btn)

class AnalysisWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Análisis Básico")
        self.setGeometry(400, 400, 800, 600)

        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        content = QWidget()
        scroll_layout = QVBoxLayout(content)

        # Estadísticas descriptivas
        stats = self.data.describe().reset_index()
        self.add_table(scroll_layout, "Estadísticas", stats)

        # Tipos de datos
        dtype_df = pd.DataFrame(self.data.dtypes.reset_index())
        dtype_df.columns = ['Columna', 'Tipo de Dato']
        self.add_table(scroll_layout, "Tipos de Datos", dtype_df)

        # Valores faltantes
        missing_df = pd.DataFrame(self.data.isnull().sum()).reset_index()
        missing_df.columns = ['Columna', 'Valores Faltantes']
        self.add_table(scroll_layout, "Valores Faltantes", missing_df)

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def add_table(self, layout, title, df):
        layout.addWidget(QLabel(f"<b>{title}</b>"))
        table = QTableWidget()
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns.tolist())

        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        layout.addWidget(table)

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(facecolor='#2d2d2d')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.setup_controls()
        self.setup_layout()

        # Conectar señales de cambio
        self.x_selector.currentTextChanged.connect(parent.update_graph)
        self.y_selector.currentTextChanged.connect(parent.update_graph)
        self.graph_type.currentTextChanged.connect(parent.update_graph)

    def setup_controls(self):
        self.controls = QWidget()
        control_layout = QHBoxLayout(self.controls)

        self.x_selector = QComboBox()
        self.y_selector = QComboBox()
        self.graph_type = QComboBox()
        self.graph_type.addItems(["Líneas", "Barras", "Dispersión", "Histograma", "Boxplot"])

        control_layout.addWidget(QLabel("Eje X:"))
        control_layout.addWidget(self.x_selector)
        control_layout.addWidget(QLabel("Eje Y:"))
        control_layout.addWidget(self.y_selector)
        control_layout.addWidget(QLabel("Tipo:"))
        control_layout.addWidget(self.graph_type)

    def setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.controls)
        layout.addWidget(self.canvas)

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.current_file = None
        self.thread = None
        self.graph_widget = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("App de Análisis de Datos")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icons/analysis.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        self.setup_sidebar(main_layout)
        self.setup_main_content(main_layout)

    def setup_sidebar(self, main_layout):
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMinimumWidth(250)

        buttons = [
            ("Cargar Datos", "icons/load.png", self.load_data),
            ("Buscar/Reemplazar", "icons/search.png", self.search_replace),
            ("Añadir Datos", "icons/add.png", self.add_data),
            ("Análisis Básico", "icons/analysis.png", self.show_basic_analysis),
            ("Generar Gráfica", "icons/graph.png", self.generate_graph),
            ("Guardar Como", "icons/save.png", self.save_as),
            ("Volver a tabla", "icons/back.png", self.show_table)
        ]

        for text, icon, handler in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setMinimumSize(220, 50)
            btn.clicked.connect(handler)
            left_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        left_layout.addStretch()
        main_layout.addWidget(left_panel, 2)

    def setup_main_content(self, main_layout):
        self.stacked_widget = QStackedWidget()
        self.table_widget = QTableWidget()
        self.stacked_widget.addWidget(self.table_widget)
        main_layout.addWidget(self.stacked_widget, 5)

    def load_data(self):
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo",
            "",
            "Archivos de Datos (*.xlsx *.xls *.csv)"
        )

        if file_path:
            self.current_file = file_path
            self.thread = DataLoaderThread(file_path)
            self.thread.loaded.connect(self.on_data_loaded)
            self.thread.error.connect(self.show_error)
            self.thread.start()

    def on_data_loaded(self, df):
        self.data = df
        self.populate_table()
        QMessageBox.information(
            self,
            "Éxito",
            f"Datos cargados correctamente\nRegistros: {len(df)}"
        )

    def populate_table(self):
        if self.data is not None:
            self.table_widget.clear()
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

            self.table_widget.setRowCount(len(self.data))
            self.table_widget.setColumnCount(len(self.data.columns))
            self.table_widget.setHorizontalHeaderLabels(self.data.columns.tolist())

            for row_idx, row in self.data.iterrows():
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row_idx, col_idx, item)

    def search_replace(self):
        if self.data is not None:
            dialog = SearchReplaceDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    search = dialog.search_input.text()
                    replace = dialog.replace_input.text()
                    case = dialog.case_checkbox.isChecked()

                    self.data.replace(
                        to_replace=search,
                        value=replace,
                        regex=False,
                        case=case,
                        inplace=True
                    )
                    self.populate_table()
                    QMessageBox.information(self, "Éxito", "Reemplazo completado")
                except Exception as e:
                    self.show_error(str(e))

    def add_data(self):
        if self.data is not None:
            dialog = AddDataDialog(self.data.columns.tolist(), self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    new_row = {col: dialog.inputs[col].text() for col in self.data.columns}
                    new_df = pd.DataFrame([new_row])
                    self.data = pd.concat([self.data, new_df], ignore_index=True)
                    self.populate_table()
                    QMessageBox.information(self, "Éxito", "Registro añadido exitosamente")
                except Exception as e:
                    self.show_error(str(e))

    def save_as(self):
        if self.data is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Como",
                "",
                "CSV Files (*.csv);;Excel Files (*.xlsx)"
            )

            if file_path:
                try:
                    if file_path.endswith(".csv"):
                        self.data.to_csv(file_path, index=False)
                    else:
                        self.data.to_excel(file_path, index=False)
                    QMessageBox.information(
                        self,
                        "Éxito",
                        f"Datos guardados en:\n{file_path}"
                    )
                except Exception as e:
                    self.show_error(str(e))

    def show_basic_analysis(self):
        if self.data is not None:
            AnalysisWindow(self.data, self).exec()

    def generate_graph(self):
        if self.data is not None:
            try:
                if self.graph_widget is None:
                    self.graph_widget = GraphWidget(self)
                    self.stacked_widget.addWidget(self.graph_widget)

                numeric_cols = self.data.select_dtypes(include=np.number).columns.tolist()

                if not numeric_cols:
                    raise ValueError("No hay columnas numéricas para graficar")

                # Actualizar selectores
                current_x = self.graph_widget.x_selector.currentText()
                current_y = self.graph_widget.y_selector.currentText()

                self.graph_widget.x_selector.clear()
                self.graph_widget.y_selector.clear()
                self.graph_widget.x_selector.addItems(numeric_cols)
                self.graph_widget.y_selector.addItems([''] + numeric_cols)  # Permitir vacío

                # Restaurar selección previa si existe
                if current_x in numeric_cols:
                    self.graph_widget.x_selector.setCurrentText(current_x)
                if current_y in numeric_cols:
                    self.graph_widget.y_selector.setCurrentText(current_y)

                self.update_graph()
                self.stacked_widget.setCurrentWidget(self.graph_widget)

            except Exception as e:
                self.show_error(str(e))

    def update_graph(self):
        try:
            if not self.graph_widget:
                return

            ax = self.graph_widget.figure.gca()
            ax.clear()

            x_col = self.graph_widget.x_selector.currentText()
            y_col = self.graph_widget.y_selector.currentText()
            graph_type = self.graph_widget.graph_type.currentText()

            # Validación de parámetros obligatorios
            if not x_col:
                raise ValueError("Debe seleccionar al menos una columna para el eje X")

            x = self.data[x_col].dropna()
            y = self.data[y_col].dropna() if y_col else None

            # Configurar colores para tema oscuro
            text_color = 'white'
            accent_color = '#2aa198'

            # Configurar gráfico según tipo
            if graph_type == "Líneas":
                if not y_col:
                    raise ValueError("Se requiere una columna Y para gráficos de líneas")
                ax.plot(x, y, color=accent_color, linewidth=2)
                ax.set_ylabel(y_col, color=text_color)

            elif graph_type == "Barras":
                if not y_col:
                    raise ValueError("Se requiere una columna Y para gráficos de barras")
                ax.bar(x, y, color=accent_color)
                ax.set_ylabel(y_col, color=text_color)

            elif graph_type == "Dispersión":
                if not y_col:
                    raise ValueError("Se requiere una columna Y para gráficos de dispersión")
                ax.scatter(x, y, color=accent_color, alpha=0.7)
                ax.set_ylabel(y_col, color=text_color)

            elif graph_type == "Histograma":
                ax.hist(x, bins='auto', color=accent_color, edgecolor='white')

            elif graph_type == "Boxplot":
                if not y_col:
                    raise ValueError("Se requiere una columna Y para gráficos de boxplot")
                ax.boxplot([x, y],
                           patch_artist=True,
                           boxprops=dict(facecolor=accent_color),
                           medianprops=dict(color='white'))

            else:
                raise ValueError("Tipo de gráfico no reconocido")

            # Configuración común del gráfico
            ax.set_title(f"{graph_type}: {x_col}" + (f" vs {y_col}" if y_col else ""),
                         color=text_color, pad=15)
            ax.set_xlabel(x_col, color=text_color)
            ax.tick_params(colors=text_color)
            ax.set_facecolor('#252525')
            ax.grid(True, linestyle='--', alpha=0.3, color='#4d4d4d')

            self.graph_widget.canvas.draw()

        except Exception as e:
            self.show_error(f"Error al generar gráfico:\n{str(e)}")

    def show_table(self):
        self.stacked_widget.setCurrentWidget(self.table_widget)

    def show_error(self, error_msg):
        QMessageBox.critical(
            self,
            "Error",
            f"Se produjo un error:\n{error_msg}",
            QMessageBox.StandardButton.Ok
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar CSS con manejo de errores
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error al cargar CSS: {str(e)}")

    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        window = DataAnalysisApp()
        window.show()
        sys.exit(app.exec())