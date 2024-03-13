import logging
from datetime import datetime
from io import TextIOWrapper
from sqlescapy import sqlescape
from .base import BaseGenerator

INTERVAL_TABLE = 'meter_readings'
NMI_COLUMN = 'nmi'
TIMESTAMP_COLUMN = 'timestamp'
CONSUMPTION_COLUMN = 'consumption'

class SQLGenerator(BaseGenerator):
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
            return

        query = f"INSERT INTO {INTERVAL_TABLE} ({NMI_COLUMN},{TIMESTAMP_COLUMN},{CONSUMPTION_COLUMN}) VALUES"

        first = True
        for i in self.interval_data:
            if not first:
                query = query + ','
            query = query + f"('{sqlescape(nmi)}', '{sqlescape(i[0].isoformat())}', {i[1]})"
            first = False

        query = query + ";\r\n"

        self.output_file.write(query)
        logging.debug(query)
        self.interval_data = []
        