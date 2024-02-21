import pytest
from fastapi.testclient import TestClient
from api.main import app
import os

from pathlib import Path
client = TestClient(app)
BASE_DIR = Path(__file__).resolve(strict=True).parent

# Liste des chemins d'image pour les tests
valid_images_to_test = [
    f"./tests/WhatsApp Image 2024-01-06 at 10.01.45.jpeg"
]
# verify that all images exist
for image_path in valid_images_to_test:
    assert os.path.exists(image_path), f"Image {image_path} does not exist."

def test_health_endpoint():
    response = client.get("/detect/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.parametrize("sample_image", valid_images_to_test)
def test_detect_endpoint_with_valid_image(sample_image):

    with open(sample_image, "rb") as image:
        response = client.post(
            "detect/image",
            files={"file": (image.name, image, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    assert 'count' in data
    assert 'detections' in data
    assert 'out_image_path' in data

    detection = data['detections'][0]
    assert 'cls' in detection
    assert 'conf' in detection


@pytest.mark.parametrize("confidence", [0.3, 0.5])
@pytest.mark.parametrize("sample_image", valid_images_to_test[:1])
def test_detect_endpoint_with_valid_image_and_confidence(sample_image, confidence):
    with open(sample_image, "rb") as image:
        response = client.post(
            f"detect/image?confidence={confidence}",
            files={"file": (image.name, image, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    assert 'count' in data
    assert 'detections' in data
    assert 'out_image_path' in data

@pytest.mark.parametrize("confidence", [-0.5, 2.0])
@pytest.mark.parametrize("sample_image", valid_images_to_test)
def test_detect_endpoint_with_valid_image_and_invalid_confidence(sample_image, confidence):
    with open(sample_image, "rb") as image:
        response = client.post(
            f"detect/image?confidence={confidence}",
            files={"file": (image.name, image, "image/jpeg")}
        )

    print("response.status_code",response.status_code)
    assert response.status_code == 422

@pytest.mark.parametrize("sample_image", ["./tests/invalid.txt"])
def test_detect_endpoint_with_invalid_image(sample_image):
    with open(sample_image, "rb") as image:
        response = client.post(
            "detect/image",
            files={"file": (image.name, image, "image/jpeg")}
        )
    assert response.status_code == 422


