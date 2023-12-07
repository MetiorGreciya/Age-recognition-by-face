import os
import cv2
import pandas as pd
from deepface import DeepFace

data = {
    "Name": [],
    "Age": [],
    "Gender": [],
    "Race": []
}

for file in os.listdir("images"):
    result = DeepFace.analyze(cv2.imread(f"images/{file}"),
                              actions=("age", "gender", "race"))

    data["Name"].append(file.split(".")[0])
    data["Age"].append(result[0]["age"])
    data["Gender"].append(result[0]["dominant_gender"])
    data["Race"].append(result[0]["dominant_race"])

df = pd.DataFrame(data)
print(df)

df.to_csv("people.csv")

img = cv2.imread('images/Matthew_McConaughey.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = cv2.CascadeClassifier('models/face.xml')
results = faces.detectMultiScale(gray, scaleFactor=1.5, minNeighbors= 2)

for (x, y, w, h) in results:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

cv2.imshow("Results", img)
cv2.waitKey(0)