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
vector<vector<string>> readCSV(const string& filename) {
    ifstream file(filename);
    if (!file) {
        cerr << "Error al abrir el archivo: " << filename << endl;
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
int countWordOccurrences(const vector<vector<string>>& content, const string& word) {
    int count = 0;
    for (const auto& row : content) {
        for (const auto& cell : row) {
            if (cell == word) {
                count++;
            }
        }
    }
    return count;
}

// Función para reemplazar una palabra por otra en el CSV
vector<vector<string>> replaceWord(const vector<vector<string>>& content, const string& oldWord, const string& newWord) {
    vector<vector<string>> modifiedContent = content;

    for (auto& row : modifiedContent) {
        for (auto& cell : row) {
            if (cell == oldWord) {
                cell = newWord;
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

    int occurrences = countWordOccurrences(content, wordToFind);
    cout << "La palabra '" << wordToFind << "' se encontró " << occurrences << " veces.\n";

    // 3. Preguntar si se desea reemplazar la palabra
    char replaceChoice;
    cout << "¿Deseas reemplazar esta palabra? (s/n): ";
    cin >> replaceChoice;

    vector<vector<string>> modifiedContent = content;
    if (replaceChoice == 's' || replaceChoice == 'S') {
        string newWord;
        cout << "¿Por qué palabra deseas reemplazar '" << wordToFind << "'? ";
        cin >> newWord;

        modifiedContent = replaceWord(content, wordToFind, newWord);
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