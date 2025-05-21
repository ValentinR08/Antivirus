# scanner/strategy/base_strategy.py

class ScanStrategy:
    def scan(self, file_path):
        raise NotImplementedError("Debes implementar el método scan()")
