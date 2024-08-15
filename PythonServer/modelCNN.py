from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import numpy as np
import requests
import tensorflow as tf
import os
import zipfile

app = Flask(__name__)


# def download_model_from_drive(model_id, model_path):
#     def get_confirm_token(response):
#         for key, value in response.cookies.items():
#             if key.startswith('download_warning'):
#                 return value
#         return None

#     def save_response_content(response, model_path):
#         CHUNK_SIZE = 32768

#         with open(model_path, "wb") as file:
#             for chunk in response.iter_content(CHUNK_SIZE):
#                 if chunk:  # Filter out keep-alive new chunks
#                     file.write(chunk)

#     URL = "https://docs.google.com/uc?export=download"
#     session = requests.Session()

#     response = session.get(URL, params={'id': model_id}, stream=True)
#     token = get_confirm_token(response)

#     if token:
#         params = {'id': model_id, 'confirm': token}
#         response = session.get(URL, params=params, stream=True)

#     save_response_content(response, model_path)
#     print(f"Model downloaded to {model_path}")




# # https://drive.google.com/file/d/1-CyZBUzBd2FZIvawGrRU_7xvdwmSH_GX/view?usp=sharing


# MODEL_FILE_ID = "1-CyZBUzBd2FZIvawGrRU_7xvdwmSH_GX"
# MODEL_PATH = 'WasteClassifierModel.keras'

# download_model_from_drive(MODEL_FILE_ID, MODEL_PATH)

# with zipfile.ZipFile(os.path.join(MODEL_PATH, "model.zip"), 'r') as zip_ref:
#     zip_ref.extractall(MODEL_PATH)

model = tf.keras.models.load_model('WasteDetectionModel(1).h5')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Missing Data', 400
  
    file = request.files['file']
    file_bytes = BytesIO(file.read())
    image = Image.open(file_bytes)

    image = image.resize((384,512))

    image_arr = np.array(image)/255.0
    image_arr = np.expand_dims(image_arr, 0)

    predictions = model.predict(image_arr)
    output = int(np.argmax(predictions[0]))

    if output in [0,1,2,3]:
        output = "Recyclable"
    else:
        output = "Non-Recyclable"

    print(output)
    return jsonify({'predicted_class': output})

    

if __name__ == "__main__":
    app.run(debug=True)