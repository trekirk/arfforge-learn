import arff  # Biblioteca liac-arff para manejar archivos ARFF
import pandas as pd
import argparse  # Para manejar argumentos de línea de comandos
import os  # Para manejar rutas y nombres de archivos

class ARFFLabelCombiner:
    def __init__(self, input_file, output_file=None):
        # Constructor de la clase, inicializa variables y carga el archivo ARFF
        self.input_file = input_file
        self.output_file = output_file or 'output.arff'  # Si no se proporciona, usa 'output.arff'
        self.data, self.meta = self.load_arff(input_file)  # Carga los datos y la metadata del ARFF
        # Convierte los datos a un DataFrame de pandas para facilitar su manipulación
        self.df = pd.DataFrame(self.data, columns=[attr[0] for attr in self.meta])
        self.label1 = None  # Primera etiqueta a combinar
        self.label2 = None  # Segunda etiqueta a combinar
        self.new_label_name = None  # Nombre de la nueva etiqueta combinada

    def load_arff(self, file_path):
        # Carga el archivo ARFF utilizando la biblioteca liac-arff
        with open(file_path, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']  # Extrae los datos del archivo
        meta = arff_data['attributes']  # Extrae la metadata (atributos y tipos)
        return data, meta

    def choose_labels(self):
        # Permite al usuario seleccionar dos etiquetas del archivo ARFF para combinar
        print("Atributos disponibles en el dataset:")
        for i, (name, _) in enumerate(self.meta):
            print(f"{i + 1}: {name}")  # Lista los nombres de los atributos con un índice

        while True:
            try:
                # Solicita al usuario que elija los índices de las dos etiquetas a combinar
                label1_index = int(input("Selecciona el número de la primera etiqueta a combinar: ")) - 1
                label2_index = int(input("Selecciona el número de la segunda etiqueta a combinar: ")) - 1

                # Validación de la selección
                if label1_index < 0 or label1_index >= len(self.meta) or label2_index < 0 or label2_index >= len(self.meta):
                    print("Selección inválida. Por favor, elige números válidos.")
                elif label1_index == label2_index:
                    print("No puedes seleccionar la misma etiqueta dos veces. Por favor, elige etiquetas diferentes.")
                else:
                    # Asigna las etiquetas seleccionadas a las variables correspondientes
                    self.label1 = self.meta[label1_index][0]
                    self.label2 = self.meta[label2_index][0]
                    # Crea un nombre para la nueva etiqueta combinada
                    self.new_label_name = f'{self.label1}_{self.label2}_combined'
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def combine_labels(self):
        # Combina las etiquetas seleccionadas en una nueva etiqueta dentro del DataFrame
        self.df[self.new_label_name] = self.df[self.label1].astype(str) + "_" + self.df[self.label2].astype(str)
        # Elimina las etiquetas originales del DataFrame
        self.df = self.df.drop([self.label1, self.label2], axis=1)

    def update_meta(self):
        # Actualiza la metadata para reflejar la nueva etiqueta combinada
        new_meta = [
            (name, attr_type) for (name, attr_type) in self.meta if name not in [self.label1, self.label2]
        ]
        # **Modificación**: Si ambos atributos originales son de tipo nominal, combinamos sus valores
        attr_type1 = next(attr[1] for attr in self.meta if attr[0] == self.label1)
        attr_type2 = next(attr[1] for attr in self.meta if attr[0] == self.label2)

        if isinstance(attr_type1, list) and isinstance(attr_type2, list):  # Ambos son nominales
            combined_values = [
                f"{val1}_{val2}" 
                for val1 in attr_type1
                for val2 in attr_type2
            ]
            # El nuevo atributo es nominal con los valores combinados
            new_meta.append((self.new_label_name, combined_values))
        else:
            # Si no son nominales, se define como STRING
            new_meta.append((self.new_label_name, 'STRING'))

        return new_meta

    def save_arff(self, new_meta):
        # Guarda el nuevo archivo ARFF con la metadata actualizada y los datos combinados
        arff_data = {
            'description': '',  # Descripción opcional
            'relation': os.path.splitext(os.path.basename(self.output_file))[0],  # Nombre de la relación
            'attributes': new_meta,  # Lista de atributos actualizada
            'data': self.df.values.tolist(),  # Los datos en formato de lista
        }
        with open(self.output_file, 'w') as f:
            arff.dump(arff_data, f)  # Usa liac-arff para guardar el archivo ARFF
        print(f"Archivo ARFF actualizado guardado en {self.output_file}")

    def process(self):
        # Ejecuta el proceso completo: seleccionar etiquetas, combinarlas y guardar el archivo
        self.choose_labels()
        self.combine_labels()
        new_meta = self.update_meta()
        self.save_arff(new_meta)

def main():
    # Configura y parsea los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Combina dos etiquetas en un archivo ARFF en una sola etiqueta.')
    parser.add_argument('input_file', type=str, help='Ruta al archivo ARFF de entrada')
    parser.add_argument('--output_file', type=str, help='Ruta al archivo ARFF de salida (opcional)')

    args = parser.parse_args()

    # Crea una instancia de la clase y ejecuta el proceso
    combiner = ARFFLabelCombiner(input_file=args.input_file, output_file=args.output_file)
    combiner.process()

if __name__ == "__main__":
    main()
