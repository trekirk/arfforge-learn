import os
import arff
import pandas as pd
from .file_selector import FileChooser

class ARFFInstanceCombiner:
    def __init__(self):
        self.file1 = None
        self.file2 = None
        self.data1 = None
        self.meta1 = None
        self.data2 = None
        self.meta2 = None
        self.combined_df = None
        self.file_chooser = FileChooser()

    def load_arff(self, file):
        with open(file, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']
        meta = arff_data['attributes']
        return data, meta

    def combine_instances(self):
        self.data1, self.meta1 = self.load_arff(self.file1)
        self.data2, self.meta2 = self.load_arff(self.file2)

        df1 = pd.DataFrame(self.data1, columns=[attr[0] for attr in self.meta1])
        df2 = pd.DataFrame(self.data2, columns=[attr[0] for attr in self.meta2])

        if self.meta1 != self.meta2:
            print("Error: Los archivos ARFF seleccionados tienen estructuras diferentes y no pueden combinarse.")
            return

        self.combined_df = pd.concat([df1, df2], ignore_index=True)

    def save_combined_arff(self, output_file):
        arff_data = {
            'description': '',
            'relation': os.path.splitext(os.path.basename(output_file))[0],
            'attributes': self.meta1,
            'data': self.combined_df.values.tolist(),
        }
        with open(output_file, 'w') as f:
            arff.dump(arff_data, f)
        print(f"Archivo ARFF combinado guardado en {output_file}")

    def process(self):
        # Seleccionar el primer archivo ARFF
        self.file1 = self.file_chooser.select_file("Selecciona el primer archivo ARFF")

        # Seleccionar el segundo archivo ARFF
        self.file2 = self.file_chooser.select_file("Selecciona el segundo archivo ARFF")

        # Combinar instancias
        self.combine_instances()

        # Seleccionar el archivo de salida
        output_file = self.file_chooser.save_file(
            "Selecciona la ubicación para guardar el archivo ARFF combinado")

        # Guardar el archivo combinado
        self.save_combined_arff(output_file)
