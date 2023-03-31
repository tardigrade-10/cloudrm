from flask import Flask, request, render_template, jsonify
from model import AutoencoderModel
import torch
import os
import numpy as np
from PIL import Image
import io
import base64
from data import preprocess_app
import cv2

global device
device = torch.device('cuda')

model = AutoencoderModel()
weights_path = os.path.join(os.getcwd(), 'weights/model_state_dict_512.pt')
model.load_state_dict(torch.load(weights_path))
model.to(device)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    
    input_image = preprocess_app(file)

    input_image = input_image.to(device)

    predicted_image = model(input_image)
    predicted_image = predicted_image.detach().cpu().numpy().transpose(1,2,0)
    predicted_image = np.ascontiguousarray(predicted_image)

    predicted_image = (predicted_image * 255).astype(np.uint8)
    predicted_image = Image.fromarray(predicted_image)
    predicted_image = predicted_image.resize((512, 512))

    # Encode PIL image as base64
    buffered = io.BytesIO()
    predicted_image.save(buffered, format="PNG")
    predicted_image_base64 = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({'predicted_image': predicted_image_base64})


if __name__ == '__main__':
    app.run(debug = True)