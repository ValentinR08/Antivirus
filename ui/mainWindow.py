# ui/main_window.py

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog,
    QTextEdit, QProgressBar, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scanner.scanEngine import ScanEngine

import time
import os


# Hilo para no congelar la interfaz durante el escaneo
class ScanThread(QThread):
    progress = pyqtSignal(int, str)

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self._is_running = True

    def run(self):
        total_files = sum(len(files) for _, _, files in os.walk(self.folder))
        scanned = 0

        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if not self._is_running:
                    return
                file_path = os.path.join(root, file)
                time.sleep(0.05)  # Simulación de escaneo
                scanned += 1
                self.progress.emit(int((scanned / total_files) * 100), file_path)

    def stop(self):
        self._is_running = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antivirus Py - Valentin")
        self.setGeometry(300, 300, 500, 400)
        self.engine = ScanEngine.get_instance()

        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.setFont(QFont("Arial", 10))

        self.layout = QVBoxLayout()

        self.label = QLabel("Selecciona una carpeta para escanear:")
        self.layout.addWidget(self.label)

        self.scan_button = QPushButton("🧪 Escanear carpeta")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setStyleSheet("background-color: #007acc; color: white; padding: 8px;")
        self.layout.addWidget(self.scan_button)

        self.status_label = QLabel("Estado: Esperando...")
        self.layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #252526; color: #d4d4d4;")
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

    def start_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona carpeta")
        if folder:
            self.output.clear()
            self.progress_bar.setValue(0)
            self.status_label.setText("Estado: Escaneando...")

            self.thread = ScanThread(folder)
            self.thread.progress.connect(self.update_progress)
            self.thread.start()

    def update_progress(self, percent, file_path):
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"Estado: Escaneando {file_path}")
        self.output.append(f"✔ Escaneado: {file_path}")

        if percent >= 100:
            self.status_label.setText("✅ Escaneo completado.")
