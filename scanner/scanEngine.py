# scanner/scan_engine.py

import os

class ScanEngine:
    _instance = None

    @staticmethod
    def get_instance():
        if ScanEngine._instance is None:
            ScanEngine()
        return ScanEngine._instance

    def __init__(self):
        if ScanEngine._instance is not None:
            raise Exception("Singleton. Usa get_instance()")
        else:
            ScanEngine._instance = self

    def scan_folder(self, folder_path):
        results = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                results.append(f"Escaneado: {file_path} - Limpio")
        return results
