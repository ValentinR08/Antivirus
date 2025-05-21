# scanner/strategy/signature_strategy.py

import hashlib
import json
from scanner.strategy.baseStrategy import ScanStrategy
import shutil
import os

class SignatureScanStrategy(ScanStrategy):
    def __init__(self, signature_file="scanner/signatures/virusSignatures.json", quarantineFolder = "quarantine"):
        with open(signature_file, "r") as f:
            self.signatures = json.load(f)
        self.quarantineFolder = quarantineFolder
        if not os.path.exists(self.quarantineFolder):
            os.makedirs(self.quarantineFolder)


    def scan(self, file_path):
        try:
            md5_hash = self.getMD5(file_path)
            for sig in self.signatures:
                if sig["md5"] == md5_hash:
                    result = f"⚠️ AMENAZA DETECTADA: {sig['name']} en {file_path}"
                    moveResult = self.moveToQuarantine(file_path)
                    return f"{result}\n{moveResult}"

            return f"✔ Limpio: {file_path}"
        except Exception as e:
            return f"❌ Error al escanear {file_path}: {str(e)}"

    def getMD5(self, path):
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def moveToQuarantine(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            quarantine_path = os.path.join(self.quarantine_folder, file_name)
            shutil.move(file_path, quarantine_path)
            return f"⚠️ Archivo movido a cuarentena: {quarantine_path}"
        except Exception as e:
            return f"❌ Error al mover a cuarentena: {file_path} - {e}"