import arff
import pandas as pd
import os
from .file_selector import FileChooser

class ARFFAttributeReorder:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.data = None
        self.meta = None
        self.df = None
        self.selected_attribute = None
        self.file_chooser = FileChooser()

    def load_arff(self, file_path):
        with open(file_path, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']
        meta = arff_data['attributes']
        return data, meta

    def choose_attribute(self):
        print("Atributos disponibles en el dataset:")
        for i, (name, _) in enumerate(self.meta):
            print(f"{i + 1}: {name}")

        while True:
            try:
                attribute_index = int(input("Selecciona el número del atributo que deseas mover al final: ")) - 1
                if attribute_index < 0 or attribute_index >= len(self.meta):
                    print("Selección inválida. Por favor, elige un número válido.")
                else:
                    self.selected_attribute = self.meta[attribute_index][0]
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def reorder_attributes(self):
        columns = list(self.df.columns)
        columns.remove(self.selected_attribute)
        columns.append(self.selected_attribute)
        self.df = self.df[columns]

    def update_meta(self):
        new_meta = [(name, attr_type) for (name, attr_type) in self.meta if name != self.selected_attribute]
        selected_meta = next((name, attr_type) for (name, attr_type) in self.meta if name == self.selected_attribute)
        new_meta.append(selected_meta)
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

        # Seleccionar el atributo a mover al final
        self.choose_attribute()

        # Seleccionar el archivo de salida
        self.output_file = self.file_chooser.save_file(
            "Selecciona la ubicación para guardar el archivo ARFF de salida")

        # Mover el atributo y guardar el archivo
        self.reorder_attributes()
        new_meta = self.update_meta()
        self.save_arff(new_meta)
