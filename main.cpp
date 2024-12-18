#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <filesystem>
#include <numeric>

using namespace std;
namespace fs = std::filesystem;

// Función para leer un archivo CSV
vector<vector<string>> leerCSV(const string& nombreArchivo) {
    ifstream archivo(nombreArchivo);
    if (!archivo) {
        cerr << "Error al abrir el archivo: " << nombreArchivo << endl;
        exit(1);
    }

    string linea;
    vector<vector<string>> contenido;

    // Leer línea por línea
    while (getline(archivo, linea)) {
        stringstream ss(linea);
        string item;
        vector<string> fila;

        // Dividir cada línea por comas
        while (getline(ss, item, ',')) {
            fila.push_back(item);
        }
        contenido.push_back(fila);
    }

    archivo.close();
    return contenido;
}

// Función para contar una palabra específica en el contenido del CSV
int contarPalabras(const vector<vector<string>>& contenido, const string& palabra) {
    int count = 0;
    for (const auto& fila : contenido) {
        for (const auto& celda : fila) {
            if (celda == palabra) {
                count++;
            }
        }
    }
    return count;
}

// Función para reemplazar una palabra por otra en el contenido del CSV
vector<vector<string>> reemplazarPalabra(const vector<vector<string>>& contenido, const string& palabraAnterior, const string& nuevaPalabra) {
    vector<vector<string>> contenidoModificado = contenido;

    for (auto& fila : contenidoModificado) {
        for (auto& celda : fila) {
            if (celda == palabraAnterior) {
                celda = nuevaPalabra;
            }
        }
    }

    return contenidoModificado;
}

// Función para extraer números de las columnas seleccionadas y convertirlos a tipo double
vector<double> extraerNumerosDeColumnas(const vector<vector<string>>& contenido, const vector<int>& columnas) {
    vector<double> numeros;
    for (const auto& fila : contenido) {
        for (int col : columnas) {
            // Verificar que la columna existe en la fila
            if (col < fila.size()) {
                try {
                    double num = stod(fila[col]);
                    numeros.push_back(num);
                } catch (...) {
                    // Ignorar las celdas que no sean números
                }
            }
        }
    }
    return numeros;
}

// Función para realizar una operación aritmética (suma en este caso)
double realizarOperacion(const vector<double>& numeros) {
    if (numeros.empty()) {
        cerr << "No se encontraron números en las columnas seleccionadas." << endl;
        return 0.0;
    }
    return accumulate(numeros.begin(), numeros.end(), 0.0);
}

int main() {
    string nombreArchivoEntrada;

    // 1. Solicitar al usuario el nombre del archivo CSV
    cout << "Introduce el nombre del archivo CSV con la extension (nombre.csv): ";
    cin >> nombreArchivoEntrada;

    // Verificar que el archivo tenga extensión .csv
    if (nombreArchivoEntrada.substr(nombreArchivoEntrada.find_last_of('.') + 1) != "csv") {
        cerr << "El archivo debe tener la extensión .csv" << endl;
        return 1;
    }

    // Verificar si el archivo realmente existe
    if (!fs::exists(nombreArchivoEntrada)) {
        cerr << "El archivo '" << nombreArchivoEntrada << "' no se encuentra en el sistema." << endl;
        return 1;
    }

    const string archivoOperaciones = "operaciones.txt";
    const string archivoFinal = "resultado.csv";

    // 2. Leer el archivo CSV
    vector<vector<string>> contenido = leerCSV(nombreArchivoEntrada);
    cout << "Contenido del archivo CSV:\n";
    for (const auto& fila : contenido) {
        for (const auto& celda : fila) {
            cout << celda << " ";
        }
        cout << endl;
    }

    // 3. Contar una palabra específica en el archivo CSV
    string palabraBuscar;
    cout << "\n¿Qué palabra deseas buscar en el archivo? ";
    cin >> palabraBuscar;

    int ocurrencias = contarPalabras(contenido, palabraBuscar);
    cout << "La palabra '" << palabraBuscar << "' se encontró " << ocurrencias << " veces.\n";

    // 4. Reemplazar una palabra por otra
    char reemplazarEleccion;
    cout << "¿Deseas reemplazar esta palabra? (s/n): ";
    cin >> reemplazarEleccion;

    vector<vector<string>> contenidoModificado = contenido;
    if (reemplazarEleccion == 's' || reemplazarEleccion == 'S') {
        string nuevaPalabra;
        cout << "¿Por qué palabra deseas reemplazar '" << palabraBuscar << "'? ";
        cin >> nuevaPalabra;

        contenidoModificado = reemplazarPalabra(contenido, palabraBuscar, nuevaPalabra);
        cout << "\nContenido después de reemplazar:\n";
        for (const auto& fila : contenidoModificado) {
            for (const auto& celda : fila) {
                cout << celda << " ";
            }
            cout << endl;
        }
    }

    // 5. Preguntar qué columnas desea sumar
    cout << "\nIntroduce las columnas que deseas sumar (separadas por espacio, comenzando desde 0): ";
    string inputColumnas;
    cin.ignore();  // Ignorar el salto de línea dejado por el cin anterior
    getline(cin, inputColumnas); // Leer las columnas seleccionadas
    stringstream ss(inputColumnas);
    vector<int> columnasSeleccionadas;
    int columna;
    while (ss >> columna) {
        columnasSeleccionadas.push_back(columna);
    }

    // 6. Extraer números de las columnas seleccionadas y realizar la suma
    vector<double> numeros = extraerNumerosDeColumnas(contenidoModificado, columnasSeleccionadas);
    double suma = realizarOperacion(numeros);
    cout << "La suma de los números en las columnas seleccionadas es: " << suma << endl;

    // 7. Guardar la suma en operaciones.txt
    ofstream archivoOp(archivoOperaciones);
    archivoOp << "Suma de las columnas seleccionadas: " << suma << endl;
    archivoOp.close();

    // 8. Guardar el contenido modificado en resultado.csv
    ofstream archivoResultado(archivoFinal);
    for (const auto& fila : contenidoModificado) {
        for (size_t i = 0; i < fila.size(); ++i) {
            archivoResultado << fila[i];
            if (i < fila.size() - 1) {
                archivoResultado << ",";  // Añadir la coma entre celdas
            }
        }
        archivoResultado << endl;
    }
    archivoResultado.close();

    cout << "\nProceso completado. Revisa los archivos generados: '" << archivoOperaciones
         << "' y '" << archivoFinal << "'." << endl;

    return 0;
}