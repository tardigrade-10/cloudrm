import os
import tempfile
import pytest
from ..app import app
from pathlib import Path


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Cloud Removal App' in response.data

# def test_predict(client):
#     test_image_path = str(Path(os.path.join(os.getcwd(), 'test_image.png')))
#     with tempfile.NamedTemporaryFile(suffix='.png') as f:
#         with open(test_image_path, 'rb') as test_image:
#             f.write(test_image.read())
#             f.seek(0)

#         response = client.post('/predict',
#                                data={'image': (f, test_image_path)},
#                                content_type='multipart/form-data')
        
#         assert response.status_code == 200
#         assert 'predicted_image' in response.json
#         predicted_image_base64 = response.json['predicted_image']
#         assert len(predicted_image_base64) > 0
