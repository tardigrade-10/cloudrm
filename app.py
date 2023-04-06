from flask import Flask, request, render_template, jsonify
from db_utils import insert_input, insert_pred
from model import load_model
import numpy as np
from PIL import Image
import io
import base64
from data import preprocess
import uuid
import os
from pathlib import Path

UPLOAD_FOLDER = os.path.join(os.getcwd() ,"results/app/input")
PREDS_FOLDER = os.path.join(os.getcwd() ,"results/app/preds")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREDS_FOLDER'] = PREDS_FOLDER

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # save image path to mysql and image to storage
    insert_input(file_path)
    file.save(file_path)
    
    input_image = preprocess(Path(file_path))

    model = load_model()
    predicted_image = model(input_image)
    predicted_image = predicted_image.detach().cpu().numpy().transpose(1,2,0)
    predicted_image = np.ascontiguousarray(predicted_image)

    predicted_image = (predicted_image * 255).astype(np.uint8)
    predicted_image = Image.fromarray(predicted_image)
    predicted_image = predicted_image.resize((512, 512))

    pred_file_path = os.path.join(app.config['PREDS_FOLDER'], filename)
    insert_pred(file_path, pred_file_path)

    predicted_image.save(pred_file_path)

    # Encode PIL image as base64
    buffered = io.BytesIO()
    predicted_image.save(buffered, format="PNG")
    predicted_image_base64 = base64.b64encode(buffered.getvalue()).decode()


    return jsonify({'predicted_image': predicted_image_base64})


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port="8080")