import arff
import pandas as pd
import os
from .file_selector import FileChooser

class ARFFAttributeRemover:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.data = None
        self.meta = None
        self.df = None
        self.selected_attribute = None
        self.file_chooser = FileChooser()

    def load_arff(self):
        # Cargar el archivo ARFF utilizando la biblioteca liac-arff
        with open(self.input_file, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']
        meta = arff_data['attributes']
        return data, meta

    def choose_attribute(self):
        # Permitir al usuario seleccionar un atributo para eliminarlo
        print("Atributos disponibles en el dataset:")
        for i, (name, _) in enumerate(self.meta):
            print(f"{i + 1}: {name}")
        
        while True:
            try:
                attribute_index = int(input("Selecciona el número del atributo que deseas eliminar: ")) - 1

                if attribute_index < 0 or attribute_index >= len(self.meta):
                    print("Selección inválida. Por favor, elige un número válido.")
                else:
                    self.selected_attribute = self.meta[attribute_index][0]
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def remove_attribute(self):
        # Eliminar el atributo seleccionado del DataFrame
        self.df = self.df.drop(columns=[self.selected_attribute])

    def update_meta(self):
        # Actualizar la metadata para reflejar el nuevo conjunto de atributos
        new_meta = [(name, attr_type) for (name, attr_type) in self.meta if name != self.selected_attribute]
        return new_meta

    def save_arff(self, new_meta):
        # Guardar el nuevo archivo ARFF con la metadata actualizada y los datos reorganizados
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
        # 1. Seleccionar el archivo de entrada
        self.input_file = self.file_chooser.select_file("Selecciona el archivo ARFF de entrada")

        # 2. Cargar los datos y la metadata
        self.data, self.meta = self.load_arff()
        self.df = pd.DataFrame(self.data, columns=[attr[0] for attr in self.meta])

        # 3. Seleccionar el atributo a eliminar
        self.choose_attribute()

        # 4. Seleccionar el archivo de salida
        self.output_file = self.file_chooser.save_file("Selecciona la ubicación para guardar el archivo ARFF de salida")

        # 5. Eliminar el atributo y guardar el archivo
        self.remove_attribute()
        new_meta = self.update_meta()
        self.save_arff(new_meta)

def main():
    remover = ARFFAttributeRemover()
    remover.process()

if __name__ == "__main__":
    main()
