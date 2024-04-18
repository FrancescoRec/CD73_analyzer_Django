## CD73 Inhibitor Bioactivity Prediction App

This Django application provides a convenient tool for predicting the bioactivity of CD73 inhibitors by leveraging molecular descriptors extracted from the PaDEL-Descriptor software. Through these descriptors, a machine learning model trained on the ChEMBL Database makes predictions.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd cd73-inhibitor-prediction-app
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the required Java environment and download the PaDEL-Descriptor software from PaDEL-Descriptor GitHub. Place the PaDEL-Descriptor.jar file in the root directory of the project.

## Usage

1. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

2. Access the application in your web browser at [http://127.0.0.1:8000/app/predict-molecule/](http://127.0.0.1:8000/app/predict-molecule/).

3. Perform predictions: upload a file with multiple molecules.

## Features

- **Batch Prediction:** Upload a file with multiple molecules for batch prediction.
- **Visualization:** View prediction results in an interactive table format.
- **Download:** Download the predictions in a .txt file

## Contributing

Contributions are welcomed! If you encounter any issues or have suggestions for improvement, feel free to open an issue or create a pull request.

## Credits

This application draws inspiration from the content featured on the YouTube channel of DataProfessor.
