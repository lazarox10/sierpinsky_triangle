import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider,
    QColorDialog, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

class SierpinskiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Triángulo de Sierpiński Interactivo")
        self.setGeometry(100, 100, 1200, 800)

        # Diseño principal
        self.mainLayout = QHBoxLayout(self)

        # Panel izquierdo para configuraciones
        self.optionsWidget = QWidget()
        self.optionsLayout = QVBoxLayout(self.optionsWidget)

        # Selección de tamaño del lado
        self.side_label = QLabel("Selecciona el tamaño del lado base (cm):")
        self.optionsLayout.addWidget(self.side_label)

        self.side_slider = QSlider(Qt.Orientation.Horizontal)
        self.side_slider.setMinimum(1)
        self.side_slider.setMaximum(10)
        self.side_slider.setValue(1)
        self.side_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.side_slider.setTickInterval(1)
        self.side_slider.valueChanged.connect(self.update_plot)
        self.optionsLayout.addWidget(self.side_slider)

        self.side_display = QLabel(f"Lado: {self.side_slider.value()} cm")
        self.optionsLayout.addWidget(self.side_display)

        # Selección del nivel
        self.level_label = QLabel("Selecciona el nivel:")
        self.optionsLayout.addWidget(self.level_label)

        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(0)
        self.level_slider.setMaximum(6)
        self.level_slider.setValue(3)
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

        # Tabla de datos adicionales
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["Parámetro", "Valor", "Razón por iteración"])
        self.table.setItem(0, 0, QTableWidgetItem("Número de triángulos"))
        self.table.setItem(1, 0, QTableWidgetItem("Área de cada triángulo (cm²)"))
        self.table.setItem(2, 0, QTableWidgetItem("Área total (cm²)"))
        self.table.setItem(3, 0, QTableWidgetItem("Perímetro de cada triángulo (cm)"))
        self.table.setItem(4, 0, QTableWidgetItem("Perímetro total (cm)"))

        razones = ["3", "1/4", "3/4", "1/2", "1.5"]
        for i, razon in enumerate(razones):
            self.table.setItem(i, 2, QTableWidgetItem(razon))

        self.optionsLayout.addWidget(self.table)

        # Botón para mostrar información en un popup
        self.info_button = QPushButton("Información sobre el Triángulo de Sierpiński")
        self.info_button.clicked.connect(self.show_info)
        self.optionsLayout.addWidget(self.info_button)

        self.optionsLayout.addStretch()
        self.mainLayout.addWidget(self.optionsWidget)

        # Panel derecho para visualización
        self.figure, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.mainLayout.addWidget(self.canvas)

        self.selected_color = "green"
        self.update_plot()

    def choose_color(self):
        """Permite seleccionar un color para el triángulo."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()
            self.update_plot()

    def sierpinski_triangle(self, ax, p1, p2, p3, level):
        """Dibuja el Triángulo de Sierpiński coloreando las áreas resultantes."""
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

    def update_plot(self):
        """Actualiza el gráfico y la tabla de datos."""
        level = self.level_slider.value()
        side_length = self.side_slider.value()

        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_title(f"Triángulo de Sierpiński - Nivel {level}")

        p1 = np.array([0, 0])
        p2 = np.array([side_length, 0])
        p3 = np.array([side_length / 2, (np.sqrt(3) / 2) * side_length])

        self.sierpinski_triangle(self.ax, p1, p2, p3, level)
        self.canvas.draw()

        # Actualizar la tabla de datos
        num_triangles = 3 ** level
        area_each = (np.sqrt(3) / 4) * (side_length ** 2) * (1 / 4) ** level
        area_total = (np.sqrt(3) / 4) * (side_length ** 2) * (3 / 4) ** level
        perimeter_each = side_length * (1 / 2) ** level
        perimeter_total = 3 * side_length * (1.5) ** level

        valores = [num_triangles, area_each, area_total, perimeter_each, perimeter_total]
        for i, valor in enumerate(valores):
            self.table.setItem(i, 1, QTableWidgetItem(str(round(valor, 6))))

        self.level_display.setText(f"Nivel: {level}")
        self.side_display.setText(f"Lado: {side_length} cm")

    def show_info(self):
        """Muestra información en un popup sobre el Triángulo de Sierpiński."""
        QMessageBox.information(self, "Información",
                                "🔺 **Triángulo de Sierpiński** 🔺\n\n"
                                "El Triángulo de Sierpiński es un fractal autosimilar nombrado por **Wacław Sierpiński** "
                                "(1882-1969), matemático polaco. Se genera aplicando un patrón recursivo: "
                                "a partir de un triángulo equilátero, se eliminan triángulos internos formados "
                                "por los puntos medios de los lados.\n\n"
                                "✅ **Ejemplo inicial:** Partimos de un triángulo equilátero con lado 1 cm.\n\n"
                                "📏 **Propiedades en cada iteración:**\n"
                                "🔺 Número de triángulos: se multiplica por 3.\n"
                                "🔹 Área de cada triángulo: se reduce con razón 1/4.\n"
                                "📐 Área total: disminuye con razón 3/4.\n"
                                "🔶 Perímetro de cada triángulo: disminuye con razón 1/2.\n"
                                "📏 Perímetro total: crece con razón 1.5.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SierpinskiApp()
    window.show()
    sys.exit(app.exec())
