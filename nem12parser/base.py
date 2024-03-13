from abc import ABC
from io import TextIOWrapper

class BaseParser(ABC):
    def parse(self, f: TextIOWrapper):
        pass
