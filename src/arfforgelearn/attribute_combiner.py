import arff
import pandas as pd
import os
from .file_selector import FileChooser

class ARFFLabelCombiner:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.data = None
        self.meta = None
        self.df = None
        self.label1 = None
        self.label2 = None
        self.new_label_name = None
        self.file_chooser = FileChooser()

    def load_arff(self, file_path):
        with open(file_path, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']
        meta = arff_data['attributes']
        return data, meta

    def choose_labels(self):
        print("Atributos disponibles en el dataset:")
        for i, (name, _) in enumerate(self.meta):
            print(f"{i + 1}: {name}")

        while True:
            try:
                label1_index = int(input("Selecciona el número de la primera etiqueta a combinar: ")) - 1
                label2_index = int(input("Selecciona el número de la segunda etiqueta a combinar: ")) - 1

                if label1_index < 0 or label1_index >= len(self.meta) or label2_index < 0 or label2_index >= len(self.meta):
                    print("Selección inválida. Por favor, elige números válidos.")
                elif label1_index == label2_index:
                    print("No puedes seleccionar la misma etiqueta dos veces. Por favor, elige etiquetas diferentes.")
                else:
                    self.label1 = self.meta[label1_index][0]
                    self.label2 = self.meta[label2_index][0]
                    self.new_label_name = f'{self.label1}_{self.label2}_combined'
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def combine_labels(self):
        self.df[self.new_label_name] = self.df[self.label1].astype(str) + "_" + self.df[self.label2].astype(str)
        self.df = self.df.drop([self.label1, self.label2], axis=1)

    def update_meta(self):
        new_meta = [
            (name, attr_type) for (name, attr_type) in self.meta if name not in [self.label1, self.label2]
        ]
        if isinstance(self.meta[0][1], list) and isinstance(self.meta[1][1], list):
            combined_values = [f"{val1}_{val2}" for val1 in self.meta[0][1] for val2 in self.meta[1][1]]
            new_meta.append((self.new_label_name, combined_values))
        else:
            new_meta.append((self.new_label_name, 'STRING'))
        return new_meta

    def save_arff(self, new_meta):
        arff_data = {
            'description': '',
            'relation': os.path.splitext(os.path.basename(self.output_file))[0],
            'attributes': new_meta,
            'data': self.df.values.tolist(),
        }
        with open(self.output_file, 'w') as f:
            arff.dump(arff_data, f)
        print(f"Archivo ARFF actualizado guardado en {self.output_file}")

    def process(self):
        # Seleccionar el archivo de entrada
        self.input_file = self.file_chooser.select_file("Selecciona el archivo ARFF de entrada")

        # Cargar los datos
        self.data, self.meta = self.load_arff(self.input_file)
        self.df = pd.DataFrame(self.data, columns=[attr[0] for attr in self.meta])

        # Seleccionar las etiquetas a combinar
        self.choose_labels()

        # Seleccionar el archivo de salida
        self.output_file = self.file_chooser.save_file(
            "Selecciona la ubicación para guardar el archivo ARFF de salida")

        # Combinar las etiquetas y guardar el archivo
        self.combine_labels()
        new_meta = self.update_meta()
        self.save_arff(new_meta)
