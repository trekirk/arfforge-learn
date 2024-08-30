import os
import arff  # Liac-arff library to handle ARFF files
import pandas as pd

class ARFFInstanceCombiner:
    def __init__(self):
        self.file1 = None
        self.file2 = None
        self.data1 = None
        self.meta1 = None
        self.data2 = None
        self.meta2 = None
        self.combined_df = None

    def list_files(self):
        # List all ARFF files in the current directory
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.arff')]
        print("Archivos ARFF disponibles en el directorio actual:")
        for i, file in enumerate(files, 1):
            print(f"{i}: {file}")
        return files

    def select_files(self, files):
        # Let the user select two files
        while True:
            try:
                file1_index = int(input("Selecciona el número del primer archivo: ")) - 1
                file2_index = int(input("Selecciona el número del segundo archivo: ")) - 1

                if file1_index < 0 or file1_index >= len(files) or file2_index < 0 or file2_index >= len(files):
                    print("Selección inválida. Por favor, elige números válidos.")
                elif file1_index == file2_index:
                    print("No puedes seleccionar el mismo archivo dos veces. Por favor, elige archivos diferentes.")
                else:
                    self.file1 = files[file1_index]
                    self.file2 = files[file2_index]
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

    def load_arff(self, file):
        # Load ARFF file and return data and metadata
        with open(file, 'r') as f:
            arff_data = arff.load(f)
        data = arff_data['data']
        meta = arff_data['attributes']
        return data, meta

    def combine_instances(self):
        # Combine the instances from both files
        self.data1, self.meta1 = self.load_arff(self.file1)
        self.data2, self.meta2 = self.load_arff(self.file2)

        # Convert data to DataFrames for easier manipulation
        df1 = pd.DataFrame(self.data1, columns=[attr[0] for attr in self.meta1])
        df2 = pd.DataFrame(self.data2, columns=[attr[0] for attr in self.meta2])

        # Check if the structure (columns) of both files matches
        if self.meta1 != self.meta2:
            print("Error: Los archivos ARFF seleccionados tienen estructuras diferentes y no pueden combinarse.")
            return

        # Combine the DataFrames
        self.combined_df = pd.concat([df1, df2], ignore_index=True)

    def get_output_filename(self):
        # Ask the user for the output file name
        output_file = input("Introduce el nombre del archivo ARFF de salida (incluyendo .arff) o presiona Enter para usar el nombre por defecto: ")

        if not output_file:
            # If no name is provided, combine the names of the input files
            base_name1 = os.path.splitext(os.path.basename(self.file1))[0]
            base_name2 = os.path.splitext(os.path.basename(self.file2))[0]
            output_file = f"{base_name1}_{base_name2}_combined.arff"

        return output_file

    def save_combined_arff(self, output_file):
        # Save the combined DataFrame to a new ARFF file
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
        # Main process to combine instances from two ARFF files
        files = self.list_files()
        if len(files) < 2:
            print("Error: No hay suficientes archivos ARFF en el directorio para combinar.")
            return

        self.select_files(files)
        self.combine_instances()

        if self.combined_df is not None:
            output_file = self.get_output_filename()
            self.save_combined_arff(output_file)

def main():
    combiner = ARFFInstanceCombiner()
    combiner.process()

if __name__ == "__main__":
    main()
