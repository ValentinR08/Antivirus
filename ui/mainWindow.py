# ui/main_window.py

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog,
    QTextEdit, QProgressBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scanner.scanEngine import ScanEngine

import os


class ScanThread(QThread):
    progress = pyqtSignal(int, str, str)  # % progreso, archivo, resultado

    def __init__(self, folder, engine):
        super().__init__()
        self.folder = folder
        self.engine = engine
        self._is_running = True

    def run(self):
        total_files = sum(len(files) for _, _, files in os.walk(self.folder))
        scanned = 0

        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if not self._is_running:
                    return
                file_path = os.path.join(root, file)
                result = self.engine.scan_file(file_path)
                scanned += 1
                self.progress.emit(int((scanned / total_files) * 100), file_path, result)

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
        self.threat_count = 0

    def start_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona carpeta")
        if folder:
            self.output.clear()
            self.progress_bar.setValue(0)
            self.status_label.setText("Estado: Escaneando...")
            self.threat_count = 0

            self.thread = ScanThread(folder, self.engine)
            self.thread.progress.connect(self.update_progress)
            self.thread.finished.connect(self.scan_finished)
            self.thread.start()

    def update_progress(self, percent, file_path, result):
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"Escaneando: {file_path}")

        if "⚠️ AMENAZA DETECTADA" in result:
            self.threat_count += 1
            self.output.append(f"<span style='color:#ff5c5c;'>{result}</span>")
        elif "Limpio" in result:
            self.output.append(f"<span style='color:#7fd37f;'>{result}</span>")
        else:
            self.output.append(result)

    def scan_finished(self):
        if self.threat_count > 0:
            self.status_label.setText(f"❌ Escaneo completado: {self.threat_count} amenaza(s) detectadas.")
        else:
            self.status_label.setText("✅ Escaneo completado: sin amenazas.")
