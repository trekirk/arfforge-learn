import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import arff  # Liac-arff library for handling ARFF files
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

class FileChooser(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Selecciona un archivo")
        self.set_size_request(400, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

    def select_file(self):
        dialog = Gtk.FileChooserDialog(
            title="Selecciona un archivo ARFF",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        filter_arff = Gtk.FileFilter()
        filter_arff.set_name("ARFF files")
        filter_arff.add_pattern("*.arff")
        dialog.add_filter(filter_arff)

        response = dialog.run()
        file_path = None
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()

        dialog.destroy()
        return file_path

class RandomForestModelComparison:
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

    def select_files(self):
        # Let the user select two train files and one test file using GTK file dialog
        print("Selecciona el primer archivo de entrenamiento:")
        self.train_file1 = self.file_chooser.select_file()

        print("Selecciona el segundo archivo de entrenamiento:")
        self.train_file2 = self.file_chooser.select_file()

        print("Selecciona el archivo de test:")
        self.test_file = self.file_chooser.select_file()

    def load_arff(self, file):
        # Load ARFF file and return data and metadata
        with open(file, 'r') as f:
            arff_data = arff.load(f)
        df = pd.DataFrame(arff_data['data'], columns=[attr[0] for attr in arff_data['attributes']])
        return df

    def prepare_data(self):
        # Load train and test data
        self.train_data1 = self.load_arff(self.train_file1)
        self.train_data2 = self.load_arff(self.train_file2)
        self.test_data = self.load_arff(self.test_file)

        # Assume the last column is the target variable
        self.X_train1 = self.train_data1.iloc[:, :-1]
        self.y_train1 = self.train_data1.iloc[:, -1]

        self.X_train2 = self.train_data2.iloc[:, :-1]
        self.y_train2 = self.train_data2.iloc[:, -1]

        self.X_test = self.test_data.iloc[:, :-1]
        self.y_test = self.test_data.iloc[:, -1]

    def train_models(self):
        # Train two Random Forest models with different training data
        self.model1 = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model1.fit(self.X_train1, self.y_train1)

        self.model2 = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model2.fit(self.X_train2, self.y_train2)

        print("Modelos Random Forest entrenados con éxito.")

    def evaluate_models(self):
        # Evaluate both models with the same test data
        y_pred1 = self.model1.predict(self.X_test)
        y_pred2 = self.model2.predict(self.X_test)

        print("\nEvaluación del Primer Modelo:")
        self.print_evaluation_metrics(y_pred1)

        print("\nEvaluación del Segundo Modelo:")
        self.print_evaluation_metrics(y_pred2)

    def print_evaluation_metrics(self, y_pred):
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))

        # Print confusion matrix
        print("\nConfusion Matrix:")
        print(confusion_matrix(self.y_test, y_pred))

        # Calculate and print accuracy
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"\nAccuracy: {accuracy:.4f}")

        # Calculate and print F1-Score
        fscore = f1_score(self.y_test, y_pred, average='weighted')
        print(f"F1-Score (Weighted): {fscore:.4f}")

    def process(self):
        # Main process: select files, prepare data, train models, and evaluate
        self.select_files()
        self.prepare_data()
        self.train_models()
        self.evaluate_models()

def main():
    tester = RandomForestModelComparison()
    tester.process()

if __name__ == "__main__":
    main()
