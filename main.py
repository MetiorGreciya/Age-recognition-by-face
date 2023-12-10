import os
import cv2
from deepface import DeepFace
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QCoreApplication

class ImageAnalyzerApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Analyzer App')
        self.setGeometry(100, 100, 800, 600)


        central_layout = QVBoxLayout()


        self.image_frame = QLabel(self)
        self.image_frame.setStyleSheet("""
            border: 2px solid #3498DB;
            background-color: #34495E;
        """)
        central_layout.addWidget(self.image_frame, 1)

        self.btn_open = QPushButton('Open Image', self)
        self.btn_open.clicked.connect(self.openImage)
        self.btn_open.setToolTip('Open an image for analysis')
        central_layout.addWidget(self.btn_open)


        self.btn_analyze = QPushButton('Analyze Image', self)
        self.btn_analyze.clicked.connect(self.analyzeImage)
        self.btn_analyze.setToolTip('Analyze the opened image and display results')
        central_layout.addWidget(self.btn_analyze)


        self.btn_delete = QPushButton('Delete Image', self)
        self.btn_delete.clicked.connect(self.deleteImage)
        self.btn_delete.setToolTip('Delete the currently displayed image')
        central_layout.addWidget(self.btn_delete)


        self.btn_clear = QPushButton('Clear Results', self)
        self.btn_clear.clicked.connect(self.clearResults)
        self.btn_clear.setToolTip('Clear the displayed results and delete the CSV file')
        central_layout.addWidget(self.btn_clear)


        self.face_info_layout = QVBoxLayout()
        central_layout.addLayout(self.face_info_layout, 1)

        self.setLayout(central_layout)


        self.setStyleSheet("""
            QWidget {
                background-color: #2E353F;
                color: #ECF0F1;
                font-size: 14px;
            }

            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #2980B9;
            }

            QLineEdit {
                padding: 8px;
                border: 1px solid #4A90E2;
                border-radius: 3px;
                background-color: #34495E;
                color: #ECF0F1;
            }

            QLabel {
                color: #ECF0F1;
            }
        """)


        self.face_labels = []

    def openImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', '',
                                               'Image Files (*.png *.jpg *.bmp)')
        if fname:
            pixmap = QPixmap(fname)
            self.image_frame.setPixmap(
                pixmap.scaled(self.image_frame.size(), Qt.KeepAspectRatio))
            self.image_frame.setAlignment(Qt.AlignCenter)

            self.image_path = fname

    def analyzeImage(self):
        if hasattr(self, 'image_path'):
            self.clearFaceInfo()
            self.addFaceInfo("Please wait...")

            QCoreApplication.processEvents()

            img = cv2.imread(self.image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = cv2.CascadeClassifier('models/face.xml')
            results = faces.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2)


            face_data = []

            for idx, (x, y, w, h) in enumerate(results, 1):
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)


                face_img = img[y:y + h, x:x + w].copy()
                result = DeepFace.analyze(face_img, actions=("age", "gender"))


                face_data.append({
                    "Face": idx,
                    "Age": result[0]["age"],
                    "Gender": result[0]["dominant_gender"]
                })


            self.clearFaceInfo()
            if face_data:
                for face_info in face_data:
                    info_str = f"Face {face_info['Face']}: Age - {face_info['Age']}, Gender - {face_info['Gender']}"
                    self.addFaceInfo(info_str)


                pixmap_result = QPixmap.fromImage(QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888))
                self.image_frame.setPixmap(pixmap_result.scaled(self.image_frame.size(), Qt.KeepAspectRatio))

                cv2.imshow("Results", img)
                cv2.waitKey(0)
            else:
                self.addFaceInfo("No faces detected")

    def deleteImage(self):

        self.clearFaceInfo()


        if os.path.exists("people.csv"):
            os.remove("people.csv")


        self.image_frame.clear()

    def clearResults(self):

        self.clearFaceInfo()


        if os.path.exists("people.csv"):
            os.remove("people.csv")

    def addFaceInfo(self, info_str):
        label = QLabel(info_str, self)
        self.face_labels.append(label)
        self.face_info_layout.addWidget(label)

    def clearFaceInfo(self):

        for label in self.face_labels:
            label.setParent(None)
            label.deleteLater()
        self.face_labels = []

if __name__ == '__main__':
    app = QApplication([])
    window = ImageAnalyzerApp()
    window.show()
    app.exec_()
