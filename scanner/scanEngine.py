# scanner/scan_engine.py

import os
from scanner.strategy.signatureStrategy import SignatureScanStrategy

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
            self.strategy = SignatureScanStrategy()
            ScanEngine._instance = self

    def scan_folder(self, folder_path):
        results = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                result = self.strategy.scan(file_path)
                results.append(result)
        return results
    def scan_file(self, file_path):
        return self.strategy.scan(file_path)
