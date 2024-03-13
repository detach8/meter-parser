import logging
from datetime import datetime
from io import TextIOWrapper
from .base import BaseGenerator

class CSVGenerator(BaseGenerator):
    def __init__(self, output_file: TextIOWrapper):
        self.output_file = output_file
        self.interval_data = []
        if not self.output_file.writable:
            raise PermissionError("Unable to write output file")

    def add_interval(self, timestamp: datetime, consumption: float):
        self.interval_data.append([timestamp, consumption])

    def generate_interval(self, nmi):
        if nmi == "":
            raise RuntimeError("NMI is not defined")
        
        if len(self.interval_data) == 0:
            raise RuntimeError("No interval data to generate")

        for i in self.interval_data:
            line = f"{nmi},{i[0].isoformat()},{i[1]}\r\n"
            self.output_file.write(line)
            logging.debug(line)

        self.interval_data = []
        