import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider,
    QColorDialog, QComboBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

class SierpinskiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Fractales de Sierpiński Interactivo")
        self.setGeometry(100, 100, 1200, 800)

        self.mainLayout = QHBoxLayout(self)

        self.optionsWidget = QWidget()
        self.optionsLayout = QVBoxLayout(self.optionsWidget)

        # Selector de tipo de fractal
        self.fractal_label = QLabel("Selecciona el tipo de fractal:")
        self.optionsLayout.addWidget(self.fractal_label)

        self.fractal_selector = QComboBox()
        self.fractal_selector.addItems(["Triángulo de Sierpiński", "Tetraedro de Sierpiński"])
        self.fractal_selector.currentIndexChanged.connect(self.update_plot)
        self.optionsLayout.addWidget(self.fractal_selector)

        # Selector de tamaño del lado
        self.side_label = QLabel("Selecciona el tamaño del lado (1-10 cm):")
        self.optionsLayout.addWidget(self.side_label)

        self.side_slider = QSlider(Qt.Orientation.Horizontal)
        self.side_slider.setMinimum(1)
        self.side_slider.setMaximum(10)
        self.side_slider.setValue(5)
        self.side_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.side_slider.setTickInterval(1)
        self.side_slider.valueChanged.connect(self.update_plot)
        self.optionsLayout.addWidget(self.side_slider)

        self.side_display = QLabel(f"Lado: {self.side_slider.value()} cm")
        self.optionsLayout.addWidget(self.side_display)

        # Selector de nivel
        self.level_label = QLabel("Selecciona el nivel:")
        self.optionsLayout.addWidget(self.level_label)

        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(0)
        self.level_slider.setMaximum(5)
        self.level_slider.setValue(2)
        self.level_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.level_slider.setTickInterval(1)
        self.level_slider.valueChanged.connect(self.update_plot)
        self.optionsLayout.addWidget(self.level_slider)

        self.level_display = QLabel(f"Nivel: {self.level_slider.value()}")
        self.optionsLayout.addWidget(self.level_display)

        # Selector de color
        self.color_button = QPushButton("Seleccionar Color")
        self.color_button.clicked.connect(self.choose_color)
        self.optionsLayout.addWidget(self.color_button)

        # Tabla de valores
        self.table = QTableWidget(7, 2)
        self.table.setHorizontalHeaderLabels(["Parámetro", "Valor"])
        self.table.setItem(0, 0, QTableWidgetItem("Número de figuras"))
        self.table.setItem(1, 0, QTableWidgetItem("Área de cada figura (cm²)"))
        self.table.setItem(2, 0, QTableWidgetItem("Área total (cm²)"))
        self.table.setItem(3, 0, QTableWidgetItem("Perímetro de cada figura (cm)"))
        self.table.setItem(4, 0, QTableWidgetItem("Perímetro total (cm)"))
        self.table.setItem(5, 0, QTableWidgetItem("Volumen de cada tetraedro (cm³)"))
        self.table.setItem(6, 0, QTableWidgetItem("Volumen total (cm³)"))
        self.optionsLayout.addWidget(self.table)

        self.optionsLayout.addStretch()
        self.mainLayout.addWidget(self.optionsWidget)

        # Panel derecho para visualización
        self.figure, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.mainLayout.addWidget(self.canvas)

        self.selected_color = "green"
        self.update_plot()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()
            self.update_plot()

    def sierpinski_triangle(self, ax, p1, p2, p3, level):
        if level == 0:
            triangle = np.array([p1, p2, p3])
            ax.fill(triangle[:, 0], triangle[:, 1], self.selected_color, edgecolor='k')
        else:
            mid1 = (p1 + p2) / 2
            mid2 = (p2 + p3) / 2
            mid3 = (p3 + p1) / 2
            self.sierpinski_triangle(ax, p1, mid1, mid3, level - 1)
            self.sierpinski_triangle(ax, mid1, p2, mid2, level - 1)
            self.sierpinski_triangle(ax, mid3, mid2, p3, level - 1)

    def sierpinski_tetrahedron(self, ax, p1, p2, p3, p4, level):
        if level == 0:
            faces = [[p1, p2, p3], [p1, p2, p4], [p1, p3, p4], [p2, p3, p4]]
            poly3d = Poly3DCollection(faces, facecolors=self.selected_color, edgecolors='k', linewidths=0.5, alpha=0.7)
            ax.add_collection3d(poly3d)
        else:
            mid12 = (p1 + p2) / 2
            mid13 = (p1 + p3) / 2
            mid14 = (p1 + p4) / 2
            mid23 = (p2 + p3) / 2
            mid24 = (p2 + p4) / 2
            mid34 = (p3 + p4) / 2

            self.sierpinski_tetrahedron(ax, p1, mid12, mid13, mid14, level - 1)
            self.sierpinski_tetrahedron(ax, mid12, p2, mid23, mid24, level - 1)
            self.sierpinski_tetrahedron(ax, mid13, mid23, p3, mid34, level - 1)
            self.sierpinski_tetrahedron(ax, mid14, mid24, mid34, p4, level - 1)

    def update_plot(self):
        level = self.level_slider.value()
        side_length = self.side_slider.value()
        self.figure.clear()

        if self.fractal_selector.currentText() == "Triángulo de Sierpiński":
            self.ax = self.figure.add_subplot(111)
            self.ax.set_aspect('equal')
            self.ax.axis('off')

            p1 = np.array([0, 0])
            p2 = np.array([side_length, 0])
            p3 = np.array([side_length / 2, (np.sqrt(3) / 2) * side_length])

            self.sierpinski_triangle(self.ax, p1, p2, p3, level)

            num_figuras = 3 ** level
            area_each = (np.sqrt(3) / 4) * (side_length ** 2) * (1 / 4) ** level
            area_total = (np.sqrt(3) / 4) * (side_length ** 2) * (3 / 4) ** level
            perimetro_each = 3 * side_length * (1 / 2) ** level
            perimetro_total = 3 * side_length * (1.5) ** level
            volumen_each = volumen_total = "N/A"
        else:
            self.ax = self.figure.add_subplot(111, projection='3d')
            self.ax.set_box_aspect([1, 1, 1])
            self.ax.axis("off")

            num_figuras = 4 ** level
            area_each = np.sqrt(3) * (side_length ** 2) / 4 * (1 / 4) ** level
            area_total = np.sqrt(3) * (side_length ** 2) / 4 * (3 / 4) ** level
            perimetro_each = 6 * side_length * (1 / 2) ** level
            perimetro_total = 6 * side_length * (1.5) ** level
            volumen_each = (side_length ** 3) / (6 * np.sqrt(2)) * (1 / 8) ** level
            volumen_total = (side_length ** 3) / (6 * np.sqrt(2)) * (7 / 8) ** level

            p1 = np.array([0, 0, 0])
            p2 = np.array([side_length, 0, 0])
            p3 = np.array([side_length / 2, np.sqrt(3) / 2 * side_length, 0])
            p4 = np.array([side_length / 2, np.sqrt(3) / 6 * side_length, np.sqrt(2) / 2 * side_length])



            self.sierpinski_tetrahedron(self.ax, p1, p2, p3, p4, level)
            self.ax.view_init(elev=30, azim=45)

        valores = [num_figuras, area_each, area_total, perimetro_each, perimetro_total, volumen_each, volumen_total]
        for i, valor in enumerate(valores):
            self.table.setItem(i, 1,
                               QTableWidgetItem(str(round(valor, 6) if isinstance(valor, (int, float)) else valor)))

        self.ax.set_title(f"{self.fractal_selector.currentText()} - Nivel {level}")
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SierpinskiApp()
    window.show()
    sys.exit(app.exec())
