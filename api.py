from flask import Flask, render_template, request, jsonify
import numpy as np
import base64
import cv2
import mediapipe as mp
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route("/image", methods=["POST"])
def get_image():
    image_url = request.json["image"]
    print(image_url)
    print(request)

    response = requests.get(str(image_url))
    pil_image = Image.open(BytesIO(response.content))
    print(pil_image)
    np_image = np.array(pil_image)

    with mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        if results.detections:
            print("감지됨")
            return {"result": True}
        else:
            print("경태 머리")
            return {"result": False}


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
