import logging
from datetime import datetime, timedelta
from io import TextIOWrapper
from .base import BaseParser
from outputgenerator import BaseGenerator

class NEM12Parser(BaseParser):
    def __init__(self, output_generator: BaseGenerator, create_datetime: str, from_participant: str, to_participant: str):
        self.output_generator = output_generator
        self.create_datetime = create_datetime
        self.from_participant = from_participant
        self.to_participant = to_participant
        self.nmi = None

    def parse(self, f: TextIOWrapper):
        for line in f:
            values = line.split(',')
            if (len(values) > 0): # Ignore empty lines
                logging.debug(f"Parsing line: {line}")
                match int(values[0]): # RecordIndicator is always numeric
                    case 100: self.parse_header(values)
                    case 200: self.parse_details(values)
                    case 300: self.parse_interval_data(values)
                    case 400: self.parse_interval_event(values)
                    case 500: self.parse_b2b_details(values)
                    case 900:
                        logging.info('End of data')
                        return
                    case _:
                        logging.warning(f"Ignoring invalid record: {line}")

    def parse_header(self, values: [str]):
        match values[1]:
            case 'NEM12': return
            case _: raise ImportError(f"Invalid header record (100): version header {values[1]} incorrect, expected NEM12")

    def parse_details(self, values: [str]):
        if len(values) != 10:
            raise ImportError("Invalid details record (200): Length of values out of range")

        if len(values[1]) < 10:
            raise ImportError("Invalid details record (200): NMI should be exactly 10 characters long")

        if len(values[4]) < 2:
            raise ImportError("Invalid details record (200): NMI suffix should be exactly 2 characters long")

        self.nmi = f"{values[1]}-{values[4]}"
        self.nmi_configuration = values[2]
        self.register_id = values[3]
        self.mdm_data_stream_identifier = values[5]
        self.meter_serial_number = values[6]
        self.uom = values[7]
        self.interval_length = int(values[8])
        self.intervals = int(1440 / self.interval_length) # caluclate number of intervals in 24h
        self.next_scheduled_read_date = values[9]
        self.last_interval_date = None
        logging.info(f"Processing NMI: {self.nmi} serial #{self.meter_serial_number} @ {self.uom} every {self.interval_length} minutes")

    def parse_interval_data(self, values: [str]):

        if self.nmi == None:
            raise ImportError("Invalid interval record (300): Details record (200) required")

        if (len(values) != self.intervals + 7):
            raise ImportError("Invalid interval record (300): Length of values out of range")

        try:
            interval_date = datetime.strptime(values[1], "%Y%m%d")
        except:
            raise ImportError(f"Invalid interval record: Interval date {values[1]} is not correctly formated")

        if self.last_interval_date != None and self.last_interval_date > interval_date:
            raise ImportError("Invalid interval record (300): Interval data must be in date sequential order")

        interval_time = 0
        for i in range(self.intervals):
            try:
                interval_value = float(values[i + 2])
            except:
                raise ImportError(f"Invalid interval record (300): Interval value {values[i + 2]} is not correctly formated")

            if interval_value < 0:
                raise ImportError(f"Invalid interval record (300): Interval value {interval_value} can not be negative")

            interval_time += self.interval_length
            interval_datetime = interval_date + timedelta(minutes=interval_time)
            self.output_generator.add_interval(interval_datetime, interval_value)
            logging.debug(f"Reading at {interval_datetime} = {interval_value}")

        quality_method = values[self.intervals + 2]
        reason_code = values[self.intervals + 3]
        reason_description = values[self.intervals + 4]
        update_datetime = values[self.intervals + 5]
        msats_load_datetime = values[self.intervals + 6]

        self.last_interval_date = interval_date
        self.output_generator.generate_interval(self.nmi)
        logging.info(f"Processed interval {interval_date}, quality method: {quality_method}, updated at {update_datetime}")

    def parse_interval_event(self, values: [str]):
        logging.info("Interval event record (400) is ignored for now")

    def parse_b2b_details(self, value: [str]):
        logging.info("B2B details record (500) is ignored for now")
