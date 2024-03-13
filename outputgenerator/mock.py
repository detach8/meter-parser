from datetime import datetime
from .base import BaseGenerator

class MockGenerator(BaseGenerator):
    def __init__(self):
        self.intervals = 0
        self.generated_intervals = 0

    def add_interval(self, timestamp: datetime, consumption: float):
        self.intervals += 1

    def generate_interval(self, nmi):
        self.generated_intervals += self.intervals
        self.intervals = 0
        return
