import os
import cv2
import pandas as pd
from deepface import DeepFace

data = {
    "Name": [],
    "Age": [],
    "Gender": []
}

for file in os.listdir("faces"):
    result = DeepFace.analyze(cv2.imread(f"faces/{file}"), actions=("age", "gender"))
    data["Name"].append(file.split(".")[0])
    data["Age"].append(result[0]["age"])
    data["Gender"].append(result[0]["dominant_gender"])

