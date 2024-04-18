from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import subprocess
import pickle
import os

from .forms import UploadFileForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def desc_calc():
    bashCommand = "java -Xms2G -Xmx2G -Djava -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./models/ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def make_predictions(input_data):
    if input_data.empty:
        return None, "Input data is empty. Please make sure it is non-empty and contains descriptors."
    
    try:
        model_path = os.path.join(BASE_DIR, 'models', 'cd73_model.pkl')
        load_model = pickle.load(open(model_path, 'rb'))
    except FileNotFoundError:
        return None, "Model file 'cd73_model.pkl' not found. Please make sure the file exists."

    try:
        predictions = load_model.predict(input_data)
        
        return predictions, None
    except Exception as e:
        return None, f"Error occurred during prediction: {e}"


def process_uploaded_file(uploaded_file):
    filename_txt = os.path.join(BASE_DIR, 'temp_file.txt') 
    filename_smi = os.path.join(BASE_DIR, 'temp_smiles.smi')  
    try:
        with open(filename_txt, 'wb+') as destination_txt, open(filename_smi, 'w+') as destination_smi:
            for chunk in uploaded_file.chunks():
                destination_txt.write(chunk)
                lines = chunk.decode('utf-8').split('\n')
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 1:  
                        destination_smi.write(parts[0] + '\n')
        return filename_txt, None
    except Exception as e:
        return None, None, f"Error occurred while processing uploaded file: {e}"

def predict_molecule(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            filename, error = process_uploaded_file(uploaded_file)
            if error:
                return HttpResponse(error)

            desc_calc()

            try:
                desc = pd.read_csv('models/descriptors_output.csv')
                Xlist = list(pd.read_csv('models/descriptor_list.csv').columns)
                desc_subset = desc[Xlist]
            except Exception as e:
                return HttpResponse(f"Error occurred while reading descriptor data: {e}")

            predictions, error = make_predictions(desc_subset)
            if error:
                return HttpResponse(error)

            try:
                model_path = os.path.join(BASE_DIR, 'models', 'cd73_model.pkl')
                load_model = pickle.load(open(model_path, 'rb'))
                molecule_names = pd.read_csv(filename, sep=' ', header=None)[1]

                result_df = pd.DataFrame({'Molecule Name': molecule_names, 'pIC50': predictions})
                result_df_json = result_df.to_json(index=False)
                result_html = result_df.to_html(index=False)

                return render(request, 'prediction_results.html', {'result_html': result_html, 'result_df_json': result_df_json})
            except Exception as e:
                return HttpResponse(f"Error occurred while generating result: {e}")
    else:
        form = UploadFileForm()

    return render(request, 'predict_molecule.html', {'form': form})

def download_view(request):
    if request.method == 'GET':
        result_df_json = request.GET.get('result_df_json', None)
        if result_df_json:
            try:
                result_df = pd.read_json(result_df_json)
                text_content = result_df.to_string(index=False)
                response = HttpResponse(text_content, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="data.txt"'
                return response
            except Exception as e:
                return HttpResponse(f"Error occurred while generating result: {e}")
    return HttpResponse("No data received.")
