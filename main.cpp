#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <filesystem>
#include <numeric>

/* Cambios propuestos
 * Preguntar al usuario si quiere añadir más datos y ponerlos en el documento original
 * Hacer que el usuario ingrese el nombre del archivo en lugar de que lea solo el "archivo.csv"
 * Configurar las operaciones aritmeticas para que de un resultado válido
 * Análisis de datos
 */

using namespace std;
namespace fs = std::filesystem;

// Función para leer un archivo CSV
vector<vector<string>> readCSV(const string& nombreArchivo) {
    ifstream file(nombreArchivo);
    if (!file) {
        cerr << "Error al abrir el archivo: " << nombreArchivo << endl;
        exit(1);
    }

    string line;
    vector<vector<string>> content;

    // Leer línea por línea
    while (getline(file, line)) {
        stringstream ss(line);
        string item;
        vector<string> row;

        // Dividir cada línea por comas
        while (getline(ss, item, ',')) {
            row.push_back(item);
        }
        content.push_back(row);
    }

    file.close();
    return content;
}

// Función para contar una palabra específica
int contadorPalabras(const vector<vector<string>>& content, const string& palabras) {
    int count = 0;
    for (const auto& row : content) {
        for (const auto& cell : row) {
            if (cell == palabras) {
                count++;
            }
        }
    }
    return count;
}

// Función para reemplazar una palabra por otra en el CSV
vector<vector<string>> remplazarPalabra(const vector<vector<string>>& content, const string& palabraAnterior, const string& nuevaPalabra) {
    vector<vector<string>> modifiedContent = content;

    for (auto& row : modifiedContent) {
        for (auto& cell : row) {
            if (cell == palabraAnterior) {
                cell = nuevaPalabra;
            }
        }
    }

    return modifiedContent;
}

// Función para extraer números de un CSV y convertirlos a tipo double
vector<double> extractNumbers(const vector<vector<string>>& content) {
    vector<double> numbers;
    for (const auto& row : content) {
        for (const auto& cell : row) {
            try {
                double num = stod(cell);
                numbers.push_back(num);
            } catch (...) {
                // Ignorar las celdas que no sean números
            }
        }
    }
    return numbers;
}

// Función para realizar una operación aritmética (suma en este caso)
double performOperation(const vector<double>& numbers) {
    if (numbers.empty()) {
        cerr << "No se encontraron números en el archivo." << endl;
        return 0.0;
    }
    return accumulate(numbers.begin(), numbers.end(), 0.0);
}

int main() {
    const string inputFile = "archivo.csv";
    const string operationsFile = "operaciones.txt";
    const string finalFile = "resultado.csv";

    // 1. Leer el archivo CSV
    vector<vector<string>> content = readCSV(inputFile);
    cout << "Contenido del archivo CSV:\n";
    for (const auto& row : content) {
        for (const auto& cell : row) {
            cout << cell << " ";
        }
        cout << endl;
    }

    // 2. Preguntar qué palabra buscar
    string wordToFind;
    cout << "\n¿Qué palabra deseas buscar? ";
    cin >> wordToFind;

    int occurrences = contadorPalabras(content, wordToFind);
    cout << "La palabra '" << wordToFind << "' se encontró " << occurrences << " veces.\n";

    // 3. Preguntar si se desea reemplazar la palabra
    char replaceChoice;
    cout << "¿Deseas reemplazar esta palabra? (s/n): ";
    cin >> replaceChoice;

    vector<vector<string>> modifiedContent = content;
    if (replaceChoice == 's' || replaceChoice == 'S') {
        string nuevaPalabra;
        cout << "¿Por qué palabra deseas reemplazar '" << wordToFind << "'? ";
        cin >> nuevaPalabra;

        modifiedContent = remplazarPalabra(content, wordToFind, nuevaPalabra);
        cout << "\nContenido después de reemplazar:\n";
        for (const auto& row : modifiedContent) {
            for (const auto& cell : row) {
                cout << cell << " ";
            }
            cout << endl;
        }
    }

    // 4. Extraer números y realizar una suma
    vector<double> numbers = extractNumbers(modifiedContent);
    double sum = performOperation(numbers);
    cout << "La suma de los números es: " << sum << endl;

    // 5. Guardar la suma en operaciones.txt
    ofstream opFile(operationsFile);
    opFile << "Suma de los números: " << sum << endl;
    opFile.close();

    // 6. Guardar el contenido modificado en resultado.csv
    ofstream resultFile(finalFile);
    for (const auto& row : modifiedContent) {
        for (size_t i = 0; i < row.size(); ++i) {
            resultFile << row[i];
            if (i < row.size() - 1) {
                resultFile << ",";  // Añadir la coma entre celdas
            }
        }
        resultFile << endl;
    }
    resultFile.close();

    cout << "\nProceso completado. Revisa los archivos generados: '" << operationsFile
         << "' y '" << finalFile << "'." << endl;

    return 0;
}