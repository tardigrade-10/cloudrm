from flask import Flask, request, render_template, jsonify
import mysql.connector
from model import AutoencoderModel
import torch
import os
import numpy as np
from PIL import Image
import io
import base64
from data import preprocess_app
import cv2

# global device
# device = torch.device('cuda')

def load_model():
    model = AutoencoderModel()
    weights_path = os.path.join(os.getcwd(), 'weights/model_state_dict_512.pt')
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    return model
# model.to(device)


app = Flask(__name__)

mydb = mysql.connector.connect(
    host="mysql",
    user="user",
    password="password",
)
cur = mydb.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS cloudrm_DB")
cur.close()

mydb = mysql.connector.connect(
    host="mysql",
    user="user",
    password="password",
    database="cloudrm_DB"
)

# app.config["MYSQL_HOST"] = "mysql"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "password"
# app.config["MYSQL_DB"] = "cloudrm_DB"

# mysql = MySQL(app)

cur = mydb.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS images (id INT NOT NULL AUTO_INCREMENT, input_image MEDIUMBLOB NOT NULL, predicted_image TEXT NOT NULL, PRIMARY KEY (id))")
cur.close()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    
    input_image = preprocess_app(file)

    # input_image = input_image.to(device)
    model = load_model()
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

    # storing images into db
    cur = mydb.cursor()
    cur.execute("INSERT INTO images (input_image, predicted_image) VALUES (%s, %s)", (file.read(), predicted_image_base64))
    mydb.commit()
    cur.close()

    return jsonify({'predicted_image': predicted_image_base64})


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port="8080")