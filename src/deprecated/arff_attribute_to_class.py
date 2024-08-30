import arff  # Liac-arff library for handling ARFF files
import pandas as pd
import argparse
import os

class ARFFAttributeReorder:
    def __init__(self, input_file, output_file=None):
        self.input_file = input_file
        self.output_file = output_file or 'output.arff'
        self.data, self.meta = self.load_arff(input_file)
        self.df = pd.DataFrame(self.data, columns=[attr[0] for attr in self.meta])  # Crear DataFrame con las etiquetas correctas
        self.selected_attribute = None

    def load_arff(self, file_path):
        # Carga el archivo ARFF utilizando la biblioteca liac-arff
        with open(file_path, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']
        meta = arff_data['attributes']
        return data, meta

    def choose_attribute(self):
        # Permite al usuario seleccionar un atributo para moverlo al último lugar
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
        # Mueve el atributo seleccionado al final
        columns = list(self.df.columns)
        columns.remove(self.selected_attribute)
        columns.append(self.selected_attribute)
        self.df = self.df[columns]

    def update_meta(self):
        # Actualiza la metadata para reflejar el nuevo orden de los atributos
        new_meta = [(name, attr_type) for (name, attr_type) in self.meta if name != self.selected_attribute]
        selected_meta = next((name, attr_type) for (name, attr_type) in self.meta if name == self.selected_attribute)
        new_meta.append(selected_meta)
        return new_meta

    def save_arff(self, new_meta):
        # Guarda el nuevo archivo ARFF con la metadata actualizada y los datos reorganizados
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
        # Proceso completo: seleccionar atributo, reorganizar y guardar
        self.choose_attribute()
        self.reorder_attributes()
        new_meta = self.update_meta()
        if self.output_file:
            self.save_arff(new_meta)

def main():
    parser = argparse.ArgumentParser(description='Mueve un atributo de un archivo ARFF al último lugar.')
    parser.add_argument('input_file', type=str, help='Ruta al archivo ARFF de entrada')
    parser.add_argument('--output_file', type=str, help='Ruta al archivo ARFF de salida (opcional)')

    args = parser.parse_args()

    reordener = ARFFAttributeReorder(input_file=args.input_file, output_file=args.output_file)
    reordener.process()

if __name__ == "__main__":
    main()

