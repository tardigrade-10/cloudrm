## Cloud Removal App
#### Using Convolutional Autoencoder

**Quantitative Analysis**

|               |  PSNR(Acc)  | MSE(Loss) |
| :-----------: | :----: | :---: |
|   Conv-AEM    | 25.086 |0.0041 |

Run for inference 
```bash
pip install -r requirements.txt
python predict.py --image data\RICE_DATASET\RICE1\cloudy_image\0.png --out_dir results --gpu True
```

Run app
```bash
pip install -r requirements.txt
python app.py
```

Run app using docker
```bash
1. Install docker
2. Create cloudrm_image using docker build 
3. Run -
docker-compose up 
```
