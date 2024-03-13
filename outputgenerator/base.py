from abc import ABC
from datetime import datetime

class BaseGenerator(ABC):
    def add_interval(self, timestamp: datetime, consumption: float):
        pass
    def generate_interval(self, nmi):
        pass
