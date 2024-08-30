# ARFForgeLearn

**ARFForgeLearn** is a powerful toolkit designed for manipulating ARFF files and applying machine learning algorithms, specifically Random Forests. The toolkit provides a user-friendly and interactive way to manage ARFF files, allowing users to reorder attributes, combine labels, remove attributes, and even combine instances across multiple ARFF files. Additionally, the toolkit offers functionalities for training and evaluating machine learning models using ARFF data.

## Table of Contents

- Features
- Usage
- Project Structure
- Contributing
- License

## Features

- **Attribute Reordering**: Move any attribute to the last position in an ARFF file.
- **Label Combination**: Combine two labels into one, allowing more complex label structures.
- **Attribute Removal**: Easily remove unwanted attributes from ARFF files.
- **Instance Combination**: Merge instances from two different ARFF files into one.
- **Random Forest Model Comparison**: Train and evaluate Random Forest models using different ARFF datasets.
- **Interactive File Selection**: A GTK-based GUI for selecting input and output files, integrated seamlessly with terminal operations.

## Usage

### Running the Main Script

To start using ARFForgeLearn, navigate to the `scripts/` directory and run the main script.

```bash
./arfforgelearn_node
```

### Available Functionalities

Once the script is running, you will be prompted to select one of the following functionalities:

1. **Move an Attribute to the End**: Reorder attributes in an ARFF file.
2. **Combine Two Labels**: Merge two labels into one within an ARFF file.
3. **Remove an Attribute**: Delete an unwanted attribute from an ARFF file.
4. **Combine Instances**: Merge instances from two ARFF files.
5. **Train and Evaluate Random Forest Models**: Use ARFF datasets to train and compare Random Forest models.

### Example Workflow

1. **Reordering an Attribute**:
   - Choose option 1 to move an attribute to the end.
   - Select the input ARFF file.
   - Choose the attribute to move.
   - Select the output ARFF file.

2. **Removing an Attribute**:
   - Choose option 3 to remove an attribute.
   - Select the input ARFF file.
   - Choose the attribute to remove.
   - Select the output ARFF file.

## Project Structure

The project is structured as follows:

- The `scripts/` directory contains the main script to run the toolkit.
- The `src/arfforgelearn/` directory contains the core scripts:
  - `__init__.py`: Initializes the ARFForgeLearn package.
  - `attribute_reorder.py`: Script for reordering attributes.
  - `attribute_combiner.py`: Script for combining labels.
  - `attribute_remover.py`: Script for removing attributes.
  - `instance_combiner.py`: Script for combining instances from ARFF files.
  - `random_forest_test.py`: Script for training and evaluating Random Forest models.
  - `file_selector.py`: GTK-based file selector utility.

```

project_root/
├── scripts/
│   └── arfforgelearn_runner.py  # Main script to run the toolkit
└── src/
    └── arfforgelearn/
        ├── __init__.py            # Initialize the ARFForgeLearn package
        ├── attribute_reorder.py   # Script for reordering attributes
        ├── attribute_combiner.py  # Script for combining labels
        ├── attribute_remover.py   # Script for removing attributes
        ├── instance_combiner.py   # Script for combining instances from ARFF files
        ├── random_forest_test.py  # Script for training and evaluating Random Forest models
        └── file_selector.py       # GTK-based file selector utility

´´´


## Contributing

Contributions are welcome! If you'd like to contribute to ARFForgeLearn, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
