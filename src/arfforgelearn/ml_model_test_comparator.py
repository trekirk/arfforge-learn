import copy
import arff
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from .file_selector import FileChooser

class MLModelComparator:
    def __init__(self):
        self.train_file1 = None
        self.train_file2 = None
        self.test_file = None
        self.train_data1 = None
        self.train_data2 = None
        self.test_data = None
        self.X_train1 = None
        self.y_train1 = None
        self.X_train2 = None
        self.y_train2 = None
        self.X_test = None
        self.y_test = None
        self.model1 = None
        self.model2 = None
        self.file_chooser = FileChooser()

    def load_arff(self, file):
        with open(file, 'r') as f:
            arff_data = arff.load(f)
        df = pd.DataFrame(arff_data['data'], columns=[attr[0] for attr in arff_data['attributes']])
        return df

    def prepare_data(self):
        self.train_data1 = self.load_arff(self.train_file1)
        self.train_data2 = self.load_arff(self.train_file2)
        self.test_data = self.load_arff(self.test_file)

        self.X_train1 = self.train_data1.iloc[:, :-1]
        self.y_train1 = self.train_data1.iloc[:, -1]

        self.X_train2 = self.train_data2.iloc[:, :-1]
        self.y_train2 = self.train_data2.iloc[:, -1]

        self.X_test = self.test_data.iloc[:, :-1]
        self.y_test = self.test_data.iloc[:, -1]

    def train_models(self):
        self.model1 = copy.deepcopy(self.algorithm)
        self.model1.fit(self.X_train1, self.y_train1)

        self.model2 = copy.deepcopy(self.algorithm)
        self.model2.fit(self.X_train2, self.y_train2)

        print("Modelos entrenados con éxito.")

    def evaluate_models(self):
        # Mostrar los nombres de los datasets utilizados y las cantidades de muestras
        print(f"\nDataset de entrenamiento para Modelo 1: {self.train_file1} (Muestras: {len(self.y_train1)})")
        print(f"Dataset de entrenamiento para Modelo 2: {self.train_file2} (Muestras: {len(self.y_train2)})")
        print(f"Dataset de testeo: {self.test_file} (Muestras: {len(self.y_test)})")

        # Evaluar ambos modelos en el conjunto de datos de prueba
        y_pred1 = self.model1.predict(self.X_test)
        y_pred2 = self.model2.predict(self.X_test)

        print("\nEvaluación del Modelo 1:")
        self.print_evaluation_metrics(y_pred1)

        print("\nEvaluación del Modelo 2:")
        self.print_evaluation_metrics(y_pred2)

    def print_evaluation_metrics(self, y_pred):
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))

        print("\nConfusion Matrix:")
        print(confusion_matrix(self.y_test, y_pred))

        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"\nAccuracy: {accuracy:.4f}")

        fscore = f1_score(self.y_test, y_pred, average='weighted')
        print(f"F1-Score (Weighted): {fscore:.4f}")

    def process(self):
        # Selección del algoritmo de clasificación
        print("Seleccione el algoritmo de clasificación:")
        print("1: Random Forest")
        print("2: Support Vector Machine (SVM)")
        print("3: K-Nearest Neighbors (KNN)")
        print("4: Decision Tree")
        choice = input("Ingrese el número del algoritmo que desea usar: ")

        if choice == '1':
            self.algorithm = RandomForestClassifier(n_estimators=100, random_state=42)
        elif choice == '2':
            from sklearn.svm import SVC
            print("Seleccione el kernel para el SVM:")
            print("1: Linear")
            print("2: RBF")
            print("3: Polynomial")
            print("4: Sigmoid")

            kernel_choice = input("Ingrese el número del kernel que desea usar: ")

            if kernel_choice == '1':
                self.algorithm = SVC(kernel='linear', random_state=42)
            elif kernel_choice == '2':
                self.algorithm = SVC(kernel='rbf', random_state=42)
            elif kernel_choice == '3':
                # Preguntar al usuario el grado del polinomio
                degree = input("Ingrese el grado del polinomio (un número entero): ")
                try:
                    degree = int(degree)
                    self.algorithm = SVC(kernel='poly', degree=degree, random_state=42)
                except ValueError:
                    print("Grado no válido, usando grado 3 por defecto.")
                    self.algorithm = SVC(kernel='poly', degree=3, random_state=42)
            elif kernel_choice == '4':
                self.algorithm = SVC(kernel='sigmoid', random_state=42)
            else:
                print("Opción no válida, usando kernel linear por defecto.")
                self.algorithm = SVC(kernel='linear', random_state=42)
        elif choice == '3':
            from sklearn.neighbors import KNeighborsClassifier
            self.algorithm = KNeighborsClassifier(n_neighbors=5)
        elif choice == '4':
            from sklearn.tree import DecisionTreeClassifier
            self.algorithm = DecisionTreeClassifier(random_state=42)
        else:
            print("Opción no válida, usando Random Forest por defecto.")
            self.algorithm = RandomForestClassifier(n_estimators=100, random_state=42)

        # Seleccionar el primer archivo de entrenamiento
        self.train_file1 = self.file_chooser.select_file(
            "Selecciona el primer archivo de entrenamiento")

        # Seleccionar el segundo archivo de entrenamiento
        self.train_file2 = self.file_chooser.select_file(
            "Selecciona el segundo archivo de entrenamiento")

        # Seleccionar el archivo de prueba
        self.test_file = self.file_chooser.select_file(
            "Selecciona el archivo de prueba")

        # Preparar los datos, entrenar y evaluar los modelos
        self.prepare_data()
        self.train_models()
        self.evaluate_models()
