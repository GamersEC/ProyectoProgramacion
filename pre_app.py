import matplotlib
matplotlib.use('QtAgg')
import sys
import os
import re
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QFileDialog, QMessageBox,
    QStackedWidget, QDialog, QComboBox, QFormLayout, QScrollArea, QLineEdit,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

sns.set_theme(style="darkgrid")


# ======================= VENTANA DE LOGIN =======================
class LoginWindow(QDialog):
    ADMIN_PASSWORD = "admin123"  # Cambia esto por una contraseña segura

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep Health - Iniciar Sesión")
        self.setWindowIcon(QIcon("icons/logo_login.png"))
        self.setMinimumSize(400, 600)
        self.attempts = 0
        self.users_file = "data/users.xlsx"
        self.initialize_users_file()
        self.setup_ui()
        self.center_window()
        self.current_user = None  # Guarda el usuario que inicia sesión

    # ======================= INICIALIZACIÓN DE USUARIOS =======================
    def initialize_users_file(self):
        """Crea el archivo de usuarios si no existe"""
        if not os.path.exists(self.users_file):
            df = pd.DataFrame(columns=["Nombre", "Apellido", "Cargo", "Username", "Password"])
            df.to_excel(self.users_file, index=False)

    # ========================= CENTRADO DE VENTANA =========================
    def center_window(self):
        qr = self.frameGeometry()
        if self.screen():
            cp = self.screen().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    # ========================= CONFIGURACIÓN DE INTERFAZ =========================
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

        # Botones de login y registro
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Ingresar")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.check_credentials)

        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.register_user)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        # Pie de página
        footer = QLabel(
            "UNIVERSIDAD NACIONAL DE CHIMBORAZO\n"
            "Ingeniería en Ciencia de Datos e Inteligencia Artificial\n"
            "© 2024-2025"
        )
        footer.setObjectName("loginFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón de información
        info_button = QPushButton("🤓")
        info_button.setObjectName("infoButton")
        info_button.clicked.connect(self.show_info)

        # Layout para el footer y el botón de info
        footer_layout = QVBoxLayout()
        footer_layout.addWidget(footer)
        footer_layout.addWidget(info_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Contenedor para el footer y botón de info
        footer_container = QWidget()
        footer_container.setLayout(footer_layout)

        # Ensamblado final
        container_layout.addWidget(self.logo_label)
        container_layout.addWidget(title)
        container_layout.addWidget(input_frame)
        container_layout.addLayout(button_layout)
        container_layout.addStretch()

        main_layout.addWidget(container)
        main_layout.addWidget(footer_container, alignment=Qt.AlignmentFlag.AlignBottom)

    # ========================= VENTANAS DE REGISTRO =========================
    def register_user(self):
        """Ventana de registro de usuario"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Registro de Usuario")
        layout = QVBoxLayout(dialog)

        form_layout = QFormLayout()
        name_input = QLineEdit()
        surname_input = QLineEdit()
        role_input = QComboBox()
        role_input.addItems(["Administrador", "Usuario"])
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        admin_password_input = QLineEdit()
        admin_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Nombre:", name_input)
        form_layout.addRow("Apellido:", surname_input)
        form_layout.addRow("Cargo:", role_input)
        form_layout.addRow("Usuario:", username_input)
        form_layout.addRow("Contraseña:", password_input)
        form_layout.addRow("Contraseña de Administrador:", admin_password_input)

        register_button = QPushButton("Registrar")
        register_button.clicked.connect(lambda: self.process_registration(
            dialog, name_input, surname_input, role_input, username_input, password_input, admin_password_input))

        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        dialog.exec()

    def process_registration(self, dialog, name, surname, role, username, password, admin_password):
        """Procesa el registro del usuario"""
        if admin_password.text() != self.ADMIN_PASSWORD:
            QMessageBox.critical(self, "Error", "Contraseña de administrador incorrecta")
            return

        if not all([name.text(), surname.text(), username.text(), password.text()]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        try:
            df = pd.read_excel(self.users_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Nombre", "Apellido", "Cargo", "Username", "Password"])

        if username.text() in df["Username"].values:
            QMessageBox.warning(self, "Error", "El usuario ya existe")
            return

        new_user = pd.DataFrame([[name.text(), surname.text(), role.currentText(), username.text(), password.text()]],
                                columns=["Nombre", "Apellido", "Cargo", "Username", "Password"])
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_excel(self.users_file, index=False)
        QMessageBox.information(self, "Registro exitoso", "Usuario registrado correctamente")
        dialog.accept()

    # ========================= VALIDACIÓN DE CREDENCIALES =========================
    def check_credentials(self):
        """Valida las credenciales contra el archivo Excel y muestra el nombre del usuario"""
        if self.attempts >= 3:
            QMessageBox.critical(self, "Bloqueado", "Demasiados intentos fallidos")
            self.reject()
            return

        username = self.username_input.text()
        password = self.password_input.text()

        try:
            df = pd.read_excel(self.users_file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Base de datos de usuarios no encontrada")
            return

        user_data = df[(df["Username"] == username) & (df["Password"] == password)]

        if not user_data.empty:
            self.current_user = user_data.iloc[0]["Nombre"]  # Guarda el nombre del usuario
            self.current_role = user_data.iloc[0]["Cargo"]  # Guarda el cargo del usuario
            self.accept()

            # Abre la ventana de bienvenida después de un inicio de sesión exitoso
            welcome_window = WelcomeWindow(self.current_user, self.current_role)
            welcome_window.exec()

        else:
            self.attempts += 1
            remaining = 3 - self.attempts
            QMessageBox.warning(
            self,
                "Error",
                f"Credenciales incorrectas\nIntentos restantes: {remaining}"
            )

    # ========================= VENTANA DE INFORMACIÓN =========================
    def show_info(self):
        QMessageBox.information(self, "Desarrolladores", "• Verónica Argudo\n• Marcus Mayorga\n• Luis Ordoñez")

# ========================= VENTANA DE BIENVENIDA =========================
class WelcomeWindow(QDialog):
    def __init__(self, username, role):
        super().__init__()
        self.setWindowTitle("Bienvenido")
        self.setWindowIcon(QIcon("icons/logo_login.png"))
        self.setMinimumSize(300, 200)

        self.time_remaining = 3  # Tiempo inicial en segundos

        layout = QVBoxLayout(self)

        # Mensaje de bienvenida
        self.welcome_label = QLabel(f"¡Bienvenido, {username}!", self)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Cargo del usuario
        self.role_label = QLabel(f"Tu cargo: {role}", self)
        self.role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.role_label.setStyleSheet("font-size: 14px;")

        # Botón de aceptar
        self.ok_button = QPushButton("Aceptar")
        self.ok_button.clicked.connect(self.accept)

        # Temporizador (etiqueta)
        self.timer_label = QLabel(f"Cerrando en {self.time_remaining}...", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout de botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.timer_label)

        # Agregar widgets al layout principal
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.role_label)
        layout.addLayout(button_layout)

        # Iniciar temporizador de 3 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Ejecuta cada 1 segundo

    def update_timer(self):
        """Actualiza el temporizador y cierra la ventana cuando llegue a 0"""
        self.time_remaining -= 1
        self.timer_label.setText(f"Cerrando en {self.time_remaining}...")

        if self.time_remaining == 0:
            self.timer.stop()
            self.accept()  # Cierra la ventana automáticamente


# ========================= HILO PARA CARGA DE DATOS =========================
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


""""# ========================= DIÁLOGO DE BUSCAR Y REEMPLAZAR =========================
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
        layout.addWidget(self.replace_btn)"""


# ========================= DIÁLOGO PARA AÑADIR DATOS =========================
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
            if col.lower() == "sexo":
                self.inputs[col] = QComboBox()
                self.inputs[col].addItems(["Masculino", "Femenino", "Intersex"])
            else:
                self.inputs[col] = QLineEdit()

            layout.addWidget(QLabel(col))
            layout.addWidget(self.inputs[col])

        self.add_btn = QPushButton("Añadir Registro")
        self.add_btn.clicked.connect(self.collect_data)
        layout.addWidget(self.add_btn)

    def collect_data(self):
        self.new_data = {}
        for col, widget in self.inputs.items():
            if isinstance(widget, QComboBox):
                self.new_data[col] = widget.currentText()
            else:
                self.new_data[col] = widget.text()
        self.accept()


# ========================= VENTANA DE ANÁLISIS MÉDICO =========================
class AnalysisWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setup_ui()
        self.load_styles()

    def load_styles(self):
        try:
            with open("Styles/analysis_style.css", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading styles: {str(e)}")

    def detect_age_column(self):
        age_keywords = r'\b(edad|age)\b'
        numeric_cols = self.data.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            if re.search(age_keywords, col, re.IGNORECASE):
                return col
        return None

    def is_medical_indicator(self, col):
        medical_keywords = r'\b(saturación|oxígeno|presión|arterial|pulso|temperatura|imc)\b'
        return re.search(medical_keywords, col, re.IGNORECASE)

    def analyze_vital_signs(self, col, scroll_layout):
        try:
            if "saturación" in col.lower():
                avg = self.data[col].mean()
                status = "Normal (95-100%)" if 95 <= avg <= 100 else "⚠️ Anormal"
                stats = [
                    f"• {col}:",
                    f"  - Promedio: {avg:.1f}%",
                    f"  - Estado: {status}"
                ]

            elif "presión" in col.lower():
                systolic = self.data[col].str.split('/').str[0].astype(float).mean()
                diastolic = self.data[col].str.split('/').str[1].astype(float).mean()
                stats = [
                    f"• {col}:",
                    f"  - Promedio sistólica: {systolic:.1f} mmHg",
                    f"  - Promedio diastólica: {diastolic:.1f} mmHg",
                    f"  - Clasificación: {self.classify_blood_pressure(systolic, diastolic)}"
                ]

            elif "pulso" in col.lower():
                avg = self.data[col].mean()
                stats = [
                    f"• {col}:",
                    f"  - Promedio: {avg:.1f} lpm",
                    f"  - Rango normal: 60-100 lpm"
                ]

            elif "temperatura" in col.lower():
                avg = self.data[col].mean()
                fever = "⚠️ Fiebre" if avg > 37.5 else "Normal"
                stats = [
                    f"• {col}:",
                    f"  - Promedio: {avg:.1f}°C",
                    f"  - Estado: {fever}"
                ]

            elif "imc" in col.lower():
                avg = self.data[col].mean()
                stats = [
                    f"• {col}:",
                    f"  - Promedio: {avg:.1f}",
                    f"  - Clasificación: {self.classify_bmi(avg)}"
                ]

            scroll_layout.addWidget(QLabel('\n'.join(stats)))

        except Exception as e:
            print(f"Error analizando {col}: {str(e)}")

    def classify_blood_pressure(self, systolic, diastolic):
        if systolic < 120 and diastolic < 80:
            return "Normal"
        elif 120 <= systolic < 130 and diastolic < 80:
            return "Elevada"
        elif 130 <= systolic < 140 or 80 <= diastolic < 90:
            return "Hipertensión Etapa 1"
        else:
            return "⚠️ Hipertensión Etapa 2"

    def classify_bmi(self, value):
        if value < 18.5:
            return "Bajo peso"
        elif 18.5 <= value < 25:
            return "Normal"
        elif 25 <= value < 30:
            return "Sobrepeso"
        else:
            return "⚠️ Obesidad"

    def setup_ui(self):
        self.setWindowTitle("Análisis de Datos Médicos")
        self.setGeometry(400, 400, 800, 600)

        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        content = QWidget()
        scroll_layout = QVBoxLayout(content)


        # =============== DATOS DEMOGRÁFICOS ===============
        scroll_layout.addWidget(QLabel("<b>Datos Demográficos</b>"))

        # Total de pacientes
        total_pacientes = len(self.data)
        scroll_layout.addWidget(QLabel(f"• Total de pacientes: {total_pacientes}"))

        # Distribución de género
        if 'Sexo' in self.data.columns:
            gender_counts = self.data['Sexo'].value_counts()
            hombres = gender_counts.get('Masculino', 0)
            mujeres = gender_counts.get('Femenino', 0)
            intersex = total_pacientes - (hombres + mujeres)

            genero_stats = [
                f"• Distribución por género:",
                f"  - Masculino: {hombres} ({hombres/total_pacientes:.1%})",
                f"  - Femenino: {mujeres} ({mujeres/total_pacientes:.1%})",
                f"  - intersex: {intersex} ({intersex/total_pacientes:.1%})"
            ]
            scroll_layout.addWidget(QLabel('\n'.join(genero_stats)))

        # Análisis de edad
        age_col = self.detect_age_column()
        if age_col:
            max_age = self.data[age_col].max()
            min_age = self.data[age_col].min()
            avg_age = self.data[age_col].mean()
            edad_stats = [
                f"• Rango de edades:",
                f"  - Máxima: {max_age} años",
                f"  - Mínima: {min_age} años",
                f"  - Promedio: {avg_age:.1f} años"
            ]
            scroll_layout.addWidget(QLabel('\n'.join(edad_stats)))


        # =============== SIGNOS VITALES ===============
        scroll_layout.addWidget(QLabel("<b>Signos Vitales</b>"))
        medical_cols = [col for col in self.data.columns if self.is_medical_indicator(col)]

        for col in medical_cols:
            if self.data[col].dtype in [np.int64, np.float64]:
                self.analyze_vital_signs(col, scroll_layout)
            elif "presión" in col.lower():
                self.analyze_vital_signs(col, scroll_layout)

        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)


# ========================= VENTANA DE BUSQUEDA =========================
class SearchDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Buscar Paciente")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)

        # Grupo de búsqueda
        search_group = QWidget()
        search_layout = QVBoxLayout(search_group)

        # Selector de tipo de búsqueda
        self.search_type = QComboBox()
        self.search_type.addItems(["Cédula", "Nombre", "Apellido"])
        self.search_type.currentTextChanged.connect(self.update_placeholder)
        search_layout.addWidget(QLabel("Buscar por:"))
        search_layout.addWidget(self.search_type)

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese el número de cédula...")
        search_layout.addWidget(self.search_input)

        # Botón de búsqueda
        self.search_btn = QPushButton("Buscar")
        self.search_btn.clicked.connect(self.search_patient)
        search_layout.addWidget(self.search_btn)

        # Tabla de resultados
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)  # Cédula, Nombre, Apellido, Acciones
        self.results_table.setHorizontalHeaderLabels(["Cédula", "Nombre", "Apellido", "Acciones"])
        self.results_table.horizontalHeader().setStretchLastSection(True)

        # Botones de acción
        action_group = QWidget()
        action_layout = QHBoxLayout(action_group)

        self.edit_btn = QPushButton("Editar")
        self.edit_btn.clicked.connect(self.edit_selected)
        self.edit_btn.setEnabled(False)

        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.close)

        action_layout.addWidget(self.edit_btn)
        action_layout.addWidget(self.close_btn)

        # Añadir widgets al layout principal
        layout.addWidget(search_group)
        layout.addWidget(self.results_table)
        layout.addWidget(action_group)

        # Conectar selección de tabla con habilitación del botón editar
        self.results_table.itemSelectionChanged.connect(self.handle_selection)

    def update_placeholder(self):
        """Actualiza el placeholder según el tipo de búsqueda seleccionado"""
        search_type = self.search_type.currentText()
        if search_type == "Cédula":
            self.search_input.setPlaceholderText("Ingrese el número de cédula...")
        elif search_type == "Nombre":
            self.search_input.setPlaceholderText("Ingrese el nombre...")
        else:  # Apellido
            self.search_input.setPlaceholderText("Ingrese el apellido...")

    def search_patient(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un término de búsqueda")
            return

        search_type = self.search_type.currentText()
        results = pd.DataFrame()

        try:
            # Convertir a minúsculas para búsqueda insensible a mayúsculas/minúsculas
            search_term_lower = search_term.lower()

            if search_type == "Cédula":
                results = self.data[self.data['Cédula'].astype(str).str.contains(search_term, case=False)]
            elif search_type == "Nombre":
                results = self.data[self.data['Nombre'].astype(str).str.lower().str.contains(search_term_lower)]
            else:  # Apellido
                results = self.data[self.data['Apellido'].astype(str).str.lower().str.contains(search_term_lower)]

            self.display_results(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la búsqueda: {str(e)}")

    def display_results(self, results):
        self.results_table.setRowCount(0)
        if results.empty:
            QMessageBox.information(self, "Resultados", "No se encontraron coincidencias")
            return

        for index, row in results.iterrows():
            current_row = self.results_table.rowCount()
            self.results_table.insertRow(current_row)

            # Añadir datos básicos
            self.results_table.setItem(current_row, 0, QTableWidgetItem(str(row['Cédula'])))
            self.results_table.setItem(current_row, 1, QTableWidgetItem(str(row['Nombre'])))
            self.results_table.setItem(current_row, 2, QTableWidgetItem(str(row['Apellido'])))

            # Botón de editar en la última columna
            edit_btn = QPushButton("✏️")
            edit_btn.clicked.connect(lambda checked, row_idx=index: self.edit_record(row_idx))
            self.results_table.setCellWidget(current_row, 3, edit_btn)

        self.results_table.resizeColumnsToContents()

    def handle_selection(self):
        self.edit_btn.setEnabled(len(self.results_table.selectedItems()) > 0)

    def edit_selected(self):
        selected_items = self.results_table.selectedItems()
        if selected_items:
            cedula = selected_items[0].text()  # Obtener la cédula de la primera columna
            matching_rows = self.data[self.data['Cédula'].astype(str) == cedula].index
            if not matching_rows.empty:
                self.edit_record(matching_rows[0])

    def edit_record(self, row_index):
        try:
            row_data = self.data.iloc[row_index].to_dict()
            dialog = EditDialog(self.data.columns.tolist(), row_data, self)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Actualizar datos en el DataFrame principal
                new_data = {col: dialog.inputs[col].text() if isinstance(dialog.inputs[col], QLineEdit)
                else dialog.inputs[col].currentText()
                            for col in self.data.columns}

                self.data.loc[row_index] = new_data
                self.parent.data = self.data  # Actualizar datos en la ventana principal
                self.parent.populate_table()  # Actualizar la tabla principal

                # Actualizar la tabla de resultados
                self.search_patient()  # Refrescar resultados
                QMessageBox.information(self, "Éxito", "Registro actualizado correctamente")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar el registro: {str(e)}")


# ========================= VENTANA PARA REEMPLAZAR =========================
class ReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Reemplazar")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.replace_input = QLineEdit()
        form_layout.addRow("Reemplazar con:", self.replace_input)

        self.replace_btn = QPushButton("Reemplazar")
        self.replace_btn.clicked.connect(self.accept)

        layout.addLayout(form_layout)
        layout.addWidget(self.replace_btn)


# ========================= WIDGET DE GRÁFICO =========================
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
        self.graph_type.currentTextChanged.connect(self.handle_graph_type_change)

    def setup_controls(self):
        self.controls = QWidget()
        control_layout = QHBoxLayout(self.controls)

        self.x_selector = QComboBox()
        self.y_selector = QComboBox()
        self.graph_type = QComboBox()
        self.graph_type.addItems(["Líneas"])

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

    def handle_graph_type_change(self):
        """Ajustar selectores según tipo de gráfico"""
        graph_type = self.graph_type.currentText()
        if graph_type in ["Histograma", "Boxplot"]:
            self.y_selector.setCurrentText('')
            self.y_selector.setEnabled(False)
        else:
            self.y_selector.setEnabled(True)
        self.parent().update_graph()


# ========================= VENTANA DE EDICIÓN DE REGISTRO =========================
class EditDialog(QDialog):
    def __init__(self, columns, data, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.data = data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Editar Registro")
        self.setFixedSize(450, 550)

        layout = QVBoxLayout(self)
        self.inputs = {}

        for col in self.columns:
            if col.lower() == "sexo":
                self.inputs[col] = QComboBox()
                self.inputs[col].addItems(["Masculino", "Femenino", "Intersex"])
                self.inputs[col].setCurrentText(str(self.data[col]))
            else:
                self.inputs[col] = QLineEdit(str(self.data[col]))

            layout.addWidget(QLabel(col))
            layout.addWidget(self.inputs[col])

        self.save_btn = QPushButton("Guardar Cambios")
        self.save_btn.clicked.connect(self.collect_data)
        layout.addWidget(self.save_btn)

    def collect_data(self):
        self.updated_data = {}
        for col, widget in self.inputs.items():
            if isinstance(widget, QComboBox):
                self.updated_data[col] = widget.currentText()
            else:
                self.updated_data[col] = widget.text()
        self.accept()


# ======================= VENTANA PRINCIPAL =======================
class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = pd.DataFrame()  # DataFrame vacío por defecto
        self.current_file = None
        self.thread = None
        self.graph_widget = None
        self.setup_ui()

    # Crear un nuevo documento con las columnas estándar
    def new_document(self):
        """Crea un nuevo documento con la estructura base requerida"""
        columns = [
            "Cédula", "Nombre", "Apellido", "Edad", "Sexo",
            "Saturación_Oxígeno", "Presión_Arterial",
            "Pulso", "Temperatura", "IMC"
        ]

        self.data = pd.DataFrame(columns=columns)
        self.current_file = None  # Reinicia la ruta actual
        self.populate_table()

        QMessageBox.information(
            self,
            "Nuevo registro",
            "Nuevo registro creado con las columnas requeridas.\n"
            "Use el botón 'Añadir Paciente' para ingresar la información del nuevo paciente."
        )

        # Configura la interfaz de usuario principal de la aplicación
    def setup_ui(self):
        self.setWindowTitle("Deep Health - Análisis de Datos Médicos")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icons/logo_login.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        self.setup_sidebar(main_layout)
        self.setup_main_content(main_layout)

    # Configura la barra lateral con botones para diferentes acciones
    def setup_sidebar(self, main_layout):
        left_panel = QWidget()
        left_panel.setMinimumWidth(250)

        # Layout principal del panel izquierdo
        left_main_layout = QVBoxLayout(left_panel)
        left_main_layout.setContentsMargins(10, 10, 10, 10)

        # Widget contenedor para los botones (centrado verticalmente)
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)

        # Lista de botones con texto, icono y acción
        buttons = [
            ("Nuevo Registro", "icons/new.png", self.new_document),  # Nuevo botón
            ("Cargar Registro", "icons/load.png", self.load_data),
            ("Editar Paciente", "icons/edit.png", self.edit_data),
            ("Buscar Paciente", "icons/search.png", self.search_replace),
            ("Añadir Paciente", "icons/add.png", self.add_data),
            ("Análisis Básico", "icons/analysis.png", self.show_basic_analysis),
            ("Generar Gráfica", "icons/graph.png", self.generate_graph),
            ("Guardar Como", "icons/save.png", self.save_as),
            ("Volver a tabla", "icons/back.png", self.show_table)
        ]

        # Crear botones con los iconos y las acciones asociadas
        for text, icon, handler in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setMinimumSize(200, 45)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )
            btn.clicked.connect(handler)
            button_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir el contenedor de botones al panel izquierdo
        left_main_layout.addStretch()
        left_main_layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        left_main_layout.addStretch()

        main_layout.addWidget(left_panel)

    # Configura el contenido principal con un widget de tabla
    def setup_main_content(self, main_layout):
        self.stacked_widget = QStackedWidget()
        self.table_widget = QTableWidget()
        self.stacked_widget.addWidget(self.table_widget)
        main_layout.addWidget(self.stacked_widget, 5)

    # Cargar los datos desde un archivo seleccionado por el usuario
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

    # Procesar los datos cargados con éxito
    def on_data_loaded(self, df):
        self.data = df
        self.populate_table()
        QMessageBox.information(
            self,
            "Éxito",
            f"Datos cargados correctamente\nRegistros: {len(df)}"
        )

    # Población de la tabla con los datos
    def populate_table(self):
        if self.data is not None:
            self.table_widget.clear()
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

            # Configurar las columnas basadas en los datos
            self.table_widget.setColumnCount(len(self.data.columns))
            self.table_widget.setHorizontalHeaderLabels(self.data.columns.tolist())

            # Llenar la tabla con los datos si existen
            if not self.data.empty:
                self.table_widget.setRowCount(len(self.data))
                for row_idx, row in self.data.iterrows():
                    for col_idx, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.table_widget.setItem(row_idx, col_idx, item)

    # Iniciar el diálogo de búsqueda y reemplazo
    def search_replace(self):
        if self.data is None:
            QMessageBox.warning(self, "Advertencia", "Primero cargue un conjunto de datos")
            return

        dialog = SearchDialog(self.data, self)
        dialog.exec()

    # Realizar la operación de reemplazo en los datos
    def perform_replace(self, search_text, replace_text, case_sensitive):
        try:
            if case_sensitive:
                self.data.replace(
                    to_replace=search_text,
                    value=replace_text,
                    regex=False,
                    inplace=True
                )
            else:
                self.data.replace(
                    to_replace=re.compile(re.escape(search_text), re.IGNORECASE),
                    value=replace_text,
                    regex=True,
                    inplace=True
                )

            self.populate_table()
            QMessageBox.information(
                self,
                "Éxito",
                f"Reemplazo completado: '{search_text}' → '{replace_text}'"
            )
        except Exception as e:
            self.show_error(str(e))

    # Iniciar el diálogo para editar datos existentes
    def edit_data(self):
        if self.data is None or self.data.empty:
            QMessageBox.warning(self, "Advertencia", "No hay datos para editar")
            return

        selected_row = self.table_widget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un registro para editar")
            return

        try:
            # Obtener datos actuales
            row_data = self.data.iloc[selected_row].to_dict()

            # Mostrar el diálogo de edición
            dialog = EditDialog(self.data.columns.tolist(), row_data, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Actualizar datos
                new_data = {col: dialog.inputs[col].text() for col in self.data.columns}
                self.data.loc[selected_row] = new_data

                # Actualizar tabla
                for col_idx, col in enumerate(self.data.columns):
                    self.table_widget.item(selected_row, col_idx).setText(new_data[col])

                QMessageBox.information(self, "Éxito", "Registro actualizado correctamente")

        except Exception as e:
            self.show_error(str(e))

    def add_data(self):
        if self.data is not None:
            dialog = AddDataDialog(self.data.columns.tolist(), self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    new_row = {}
                    for col in self.data.columns:
                        widget = dialog.inputs[col]
                        value = widget.currentText() if isinstance(widget, QComboBox) else widget.text()

                        # Intentar conversión de tipos si la columna es numérica
                        if col in ["Edad", "Saturación_Oxígeno", "Pulso", "Temperatura", "IMC"]:
                            try:
                                new_row[col] = float(value) if '.' in value else int(value)
                            except ValueError:
                                new_row[col] = None  # Si la conversión falla, asigna None

                        else:
                            new_row[col] = value  # Para columnas de texto, mantener el valor sin cambios

                    # Añadir la fila al DataFrame
                    self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
                    self.populate_table()
                    QMessageBox.information(self, "Éxito", "Registro añadido exitosamente")

                except ValueError as ve:
                    self.show_error(f"Error de formato: {str(ve)}")
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

                # Bloquear señales durante actualización
                self.graph_widget.x_selector.blockSignals(True)
                self.graph_widget.y_selector.blockSignals(True)

                # Actualizar selectores
                current_x = self.graph_widget.x_selector.currentText()
                current_y = self.graph_widget.y_selector.currentText()

                self.graph_widget.x_selector.clear()
                self.graph_widget.x_selector.addItems(numeric_cols)

                self.graph_widget.y_selector.clear()
                self.graph_widget.y_selector.addItems([''] + numeric_cols)

                # Restaurar o establecer selecciones
                if current_x in numeric_cols:
                    self.graph_widget.x_selector.setCurrentText(current_x)
                else:
                    self.graph_widget.x_selector.setCurrentText(numeric_cols[0] if numeric_cols else '')

                # Establecer Y solo si es necesario
                if self.graph_widget.graph_type.currentText() in ["Líneas", "Barras", "Dispersión"]:
                    if current_y in numeric_cols:
                        self.graph_widget.y_selector.setCurrentText(current_y)
                    else:
                        self.graph_widget.y_selector.setCurrentText(numeric_cols[0] if numeric_cols else '')
                else:
                    self.graph_widget.y_selector.setCurrentText('')

                # Desbloquear señales
                self.graph_widget.x_selector.blockSignals(False)
                self.graph_widget.y_selector.blockSignals(False)

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
            graph_type = self.graph_widget.graph_type.currentText()

            if not x_col:
                raise ValueError("Seleccione una columna para analizar")

            # Detección de parámetros médicos
            is_medical = {
                'presión': 'Presión Arterial' in x_col,
                'saturación': 'Saturación' in x_col,
                'pulso': 'Pulso' in x_col,
                'temperatura': 'Temperatura' in x_col,
                'imc': 'IMC' in x_col
            }

            # Configuraciones comunes
            text_color = 'white'
            accent_color = '#2aa198'
            ax.set_facecolor('#252525')
            ax.tick_params(colors=text_color)
            ax.grid(True, linestyle='--', alpha=0.3, color='#4d4d4d')

            if is_medical['presión']:
                # Gráfico especial para presión arterial
                systolic = self.data[x_col].str.split('/').str[0].astype(float)
                diastolic = self.data[x_col].str.split('/').str[1].astype(float)

                ax.scatter(range(len(systolic)), systolic, color='#d73027', label='Sistólica')
                ax.scatter(range(len(diastolic)), diastolic, color='#4575b4', label='Diastólica')

                # Líneas de referencia
                ax.axhline(120, color='#d73027', linestyle='--', alpha=0.5)
                ax.axhline(80, color='#4575b4', linestyle='--', alpha=0.5)

                ax.set_title("Presión Arterial por Paciente", color=text_color, pad=15)
                ax.set_xlabel("Pacientes", color=text_color)
                ax.set_ylabel("mmHg", color=text_color)
                ax.legend()

            elif is_medical['saturación']:
                # Gráfico de saturación de oxígeno
                values = self.data[x_col]
                ax.bar(range(len(values)), values, color=accent_color)

                # Línea de referencia y anotación
                ax.axhline(95, color='red', linestyle='--', alpha=0.7)
                ax.annotate('Límite normal (95%)',
                            xy=(0, 95), xycoords='data',
                            xytext=(10, 10), textcoords='offset points',
                            color='red', fontsize=9)

                ax.set_title("Saturación de Oxígeno", color=text_color)
                ax.set_ylabel("% SpO2", color=text_color)
                ax.set_ylim(85, 100)

            elif is_medical['imc']:
                # Boxplot para IMC con categorías
                categories = [
                    'Bajo peso (<18.5)',
                    'Normal (18.5-24.9)',
                    'Sobrepeso (25-29.9)',
                    'Obesidad (≥30)'
                ]

                data = [
                    self.data[self.data[x_col] < 18.5][x_col],
                    self.data[(self.data[x_col] >= 18.5) & (self.data[x_col] < 25)][x_col],
                    self.data[(self.data[x_col] >= 25) & (self.data[x_col] < 30)][x_col],
                    self.data[self.data[x_col] >= 30][x_col]
                ]

                box = ax.boxplot(data, patch_artist=True, labels=categories)
                for patch in box['boxes']:
                    patch.set_facecolor(accent_color)

                ax.set_title("Distribución de IMC por Categoría", color=text_color)
                ax.set_ylabel("Índice de Masa Corporal", color=text_color)

            elif is_medical['temperatura']:
                # Gráfico de línea para temperatura con área
                x = range(len(self.data))
                y = self.data[x_col]

                ax.plot(x, y, color=accent_color, marker='o')
                ax.fill_between(x, y, 37.5, where=(y >= 37.5),
                                color='red', alpha=0.3, interpolate=True)
                ax.axhline(37.5, color='red', linestyle='--', label='Fiebre')

                ax.set_title("Registro de Temperatura Corporal", color=text_color)
                ax.set_ylabel("°C", color=text_color)
                ax.legend()

            elif is_medical['pulso']:
                # Histograma de frecuencia cardíaca
                sns.histplot(self.data[x_col], bins=15, kde=True,
                             color=accent_color, ax=ax)

                # Zonas de riesgo
                ax.axvline(60, color='green', linestyle='--', alpha=0.7)
                ax.axvline(100, color='orange', linestyle='--', alpha=0.7)
                ax.annotate('Bradicardia', xy=(55, 0),
                            rotation=90, color='green', alpha=0.7)
                ax.annotate('Taquicardia', xy=(105, 0),
                            rotation=90, color='orange', alpha=0.7)

                ax.set_title("Distribución de Frecuencia Cardíaca", color=text_color)
                ax.set_xlabel("Latidos por minuto", color=text_color)

            else:
                # Gráfico genérico para otras columnas
                if graph_type == "Histograma":
                    sns.histplot(self.data[x_col], bins='auto',
                                 color=accent_color, ax=ax)
                elif graph_type == "Boxplot":
                    sns.boxplot(y=self.data[x_col], color=accent_color, ax=ax)
                else:
                    y_col = self.graph_widget.y_selector.currentText()
                    if y_col:
                        sns.scatterplot(x=self.data[x_col], y=self.data[y_col],
                                        color=accent_color, ax=ax)
                        ax.set_ylabel(y_col, color=text_color)

                ax.set_title(f"{graph_type}: {x_col}", color=text_color)
                ax.set_xlabel(x_col, color=text_color)

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


# ======================= EJECUCIÓN PRINCIPAL =======================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("Styles/style.css", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error al cargar CSS: {str(e)}")

    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        window = DataAnalysisApp()
        window.show()
        sys.exit(app.exec())