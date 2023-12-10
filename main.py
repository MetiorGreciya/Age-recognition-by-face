import os
import cv2
import pandas as pd
from deepface import DeepFace
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Analyzer App')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.btn_open = QPushButton('Open Image', self)
        self.btn_open.clicked.connect(self.openImage)

        self.btn_analyze = QPushButton('Analyze Image', self)
        self.btn_analyze.clicked.connect(self.analyzeImage)

        self.name_input = QLineEdit(self)
        self.age_input = QLineEdit(self)
        self.gender_input = QLineEdit(self)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_analyze)
        layout.addWidget(QLabel('Name:'))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel('Age:'))
        layout.addWidget(self.age_input)
        layout.addWidget(QLabel('Gender:'))
        layout.addWidget(self.gender_input)

        self.setLayout(layout)

    def openImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')
        if fname:
            pixmap = QPixmap(fname)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            self.image_label.setAlignment(Qt.AlignCenter)

            self.image_path = fname

    def analyzeImage(self):
        if hasattr(self, 'image_path'):
            img = cv2.imread(self.image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = cv2.CascadeClassifier('models/face.xml')
            results = faces.detectMultiScale(gray, scaleFactor=1.5, minNeighbors= 2)

            for (x, y, w, h) in results:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

            cv2.imshow("Results", img)
            cv2.waitKey(0)

            data = {
                "Name": [self.name_input.text()],
                "Age": [result[0]["age"]],
                "Gender": [result[0]["dominant_gender"]]
            }

            df = pd.DataFrame(data)

            if os.path.exists("people.csv"):
                existing_df = pd.read_csv("people.csv")
                df = pd.concat([existing_df, df], ignore_index=True)

            df.to_csv("people.csv", index=False)

if __name__ == '__main__':
    app = QApplication([])
    window = ImageAnalyzerApp()
    window.show()
    app.exec_()