import os
import cv2
from deepface import DeepFace
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QCoreApplication

class ImageAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация пользовательского интерфейса
        self.initUI()

    def initUI(self):
        # Настройка параметров окна
        self.setWindowTitle('Image Analyzer App')
        self.setGeometry(100, 100, 800, 600)

        # Создание компоновки и стилей
        self.setupLayout()
        self.setupStyles()

        # Инициализация переменных для хранения меток лиц и пути к изображению
        self.face_labels = []
        self.image_path = None

    def setupLayout(self):
        # Создание вертикальной компоновки для размещения элементов интерфейса
        central_layout = QVBoxLayout()

        # Создание виджета для отображения изображения
        self.image_frame = self.createImageFrame()

        # Создание метки для отображения результатов анализа
        self.result_label = self.createResultLabel()

        # Создание кнопок управления приложением с подсказками
        self.btn_open = self.createButton('Open Image', self.openImage, 'Open an image file')
        self.btn_analyze = self.createButton('Analyze Image', self.analyzeImage, 'Analyze faces in the image')
        self.btn_delete = self.createButton('Delete Image', self.deleteImage, 'Delete the loaded image')
        self.btn_clear = self.createButton('Clear Results', self.clearResults, 'Clear analysis results')

        # Создание компоновки для отображения информации о лицах
        self.face_info_layout = self.createFaceInfoLayout()

        # Добавление созданных виджетов в компоновку
        central_layout.addWidget(self.image_frame, 1)
        central_layout.addWidget(self.result_label)
        central_layout.addWidget(self.btn_open)
        central_layout.addWidget(self.btn_analyze)
        central_layout.addWidget(self.btn_delete)
        central_layout.addWidget(self.btn_clear)
        central_layout.addLayout(self.face_info_layout, 1)

        # Установка созданной компоновки в качестве основной для окна
        self.setLayout(central_layout)

    def setupStyles(self):
        # Настройка стилей виджетов с использованием CSS
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

    def createImageFrame(self):
        # Создание виджета QLabel для отображения изображения
        image_frame = QLabel(self)
        image_frame.setStyleSheet("""
            border: 2px solid #3498DB;
            background-color: #34495E;
        """)
        return image_frame

    def createResultLabel(self):
        # Создание метки QLabel для отображения результатов анализа
        result_label = QLabel(self)
        result_label.setAlignment(Qt.AlignCenter)
        return result_label

    def createButton(self, text, slot, tooltip=''):
        # Создание кнопки с указанным текстом и связывание сигнала нажатия с указанным методом
        btn = QPushButton(text, self)
        btn.setToolTip(tooltip)
        btn.clicked.connect(slot)
        return btn

    def createFaceInfoLayout(self):
        # Создание вертикальной компоновки для отображения информации о лицах
        face_info_layout = QVBoxLayout()
        return face_info_layout

    def openImage(self):
        # Метод для открытия диалогового окна выбора изображения
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')
        if fname:
            # Загрузка выбранного изображения
            self.loadImage(fname)

    def loadImage(self, path):
        # Метод для загрузки изображения и отображения его в виджете QLabel
        pixmap = QPixmap(path)
        self.image_frame.setPixmap(pixmap.scaled(self.image_frame.size(), Qt.KeepAspectRatio))
        self.image_frame.setAlignment(Qt.AlignCenter)
        self.image_path = path

    def analyzeImage(self):
        # Метод для анализа изображения и отображения результатов
        if self.image_path:
            self.clearFaceInfo()
            self.addFaceInfo("Please wait...")

            QCoreApplication.processEvents()

            img = cv2.imread(self.image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = cv2.CascadeClassifier('models/face.xml')
            results = faces.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2)

            face_data = self.analyzeFaces(results, img)

            self.clearFaceInfo()
            if face_data:
                self.displayResults(face_data, img)
            else:
                self.addFaceInfo("No faces detected")
                self.result_label.clear()
        else:
            self.addFaceInfo("Please open an image first.")

    def analyzeFaces(self, results, img):
        # Метод для анализа лиц на изображении
        face_data = []

        for idx, (x, y, w, h) in enumerate(results, 1):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

            face_img = img[y:y + h, x:x + w].copy()
            face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

            result = DeepFace.analyze(face_img_rgb, actions=("age", "gender"))

            face_data.append({
                "Face": idx,
                "Age": result[0]["age"],
                "Gender": result[0]["dominant_gender"]
            })

        return face_data

    def clearFaceInfo(self):
        # Метод для удаления меток с информацией о лицах
        for label in self.face_labels:
            label.setParent(None)
            label.deleteLater()
        self.face_labels = []

    def displayResults(self, face_data, img):
        # Метод для отображения результатов анализа лиц и обновления изображения
        for face_info in face_data:
            info_str = f"Face {face_info['Face']}: Age - {face_info['Age']}, Gender - {face_info['Gender']}"
            self.addFaceInfo(info_str)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixmap_result = QPixmap.fromImage(QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], img_rgb.shape[1] * 3, QImage.Format_RGB888))
        self.image_frame.setPixmap(pixmap_result.scaled(self.image_frame.size(), Qt.KeepAspectRatio))

        result_str = f"Total Faces: {len(face_data)}"
        self.result_label.setText(result_str)

    def deleteImage(self):
        # Метод для удаления загруженного изображения и связанных результатов
        self.clearFaceInfo()

        if os.path.exists("people.csv"):
            os.remove("people.csv")

        self.image_frame.clear()
        self.result_label.clear()
        self.image_path = None

    def clearResults(self):
        # Метод для очистки результатов анализа и меток с информацией о лицах
        self.clearFaceInfo()

        if os.path.exists("people.csv"):
            os.remove("people.csv")

        self.result_label.clear()

    def addFaceInfo(self, info_str):
        # Метод для добавления метки с информацией о лице в компоновку
        label = QLabel(info_str, self)
        self.face_labels.append(label)
        self.face_info_layout.addWidget(label)

if __name__ == '__main__':
    # Запуск приложения
    app = QApplication([])
    window = ImageAnalyzerApp()
    window.show()
    app.exec_()