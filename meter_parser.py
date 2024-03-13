import os
import logging
import argparse
from nem12parser import NEM12Parser
from outputgenerator import SQLGenerator, CSVGenerator 

def parse(input_file, output_generator):
    try:
        for line in input_file:
            values = line.split(',')
            if (len(values) > 0): # Ignore empty lines
                match int(values[0]): # RecordIndicator is always numeric
                    case 100:
                        parse_header(values, input_file, output_generator)
                    case 900:
                        logging.info('End of data')
                        return
                    case _:
                        logging.warning(f"Ignoring invalid record: {line}")
    except Exception as e:
        logging.error(repr(e))
        exit(2)

def parse_header(values, input_file, output_generator):
    match values[1]:
        case 'NEM12':
            logging.info("Parsing NEM12 format")
            nem12 = NEM12Parser(output_generator, values[1], values[2], values[3])
            nem12.parse(input_file)
        case 'NEM13':
            logging.warn("NEM13 format is not supported at this time.")
        case _:
            logging.error(f"Invalid version header: {values[1]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    parser.add_argument('-o', '--output-type', choices=['sql', 'csv'], default='sql', help='Output file type')
    parser.add_argument('input_file', help='File to parse')
    parser.add_argument('output_file')
    args = parser.parse_args()

    # Verbose logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Enabling verbose logging")
    else:
        # Default loglevel
        logging.basicConfig(level=logging.INFO)

    # Check input_file
    if not os.path.isfile(args.input_file):
        logging.error(f"File {args.input_file} does not exist, is not readable, or is not a file.")
        exit(1)
    
    # If output_file is not writable, this should throw an error
    try:
        with open(args.output_file, mode='w') as output_file:
            output_generator = None
            match args.output_type:
                case 'csv':
                    output_generator = CSVGenerator(output_file)
                case 'sql':
                    output_generator = SQLGenerator(output_file)
                case _:
                    logging.error(f"Invalid output type {args.output_type}")
                    exit(1)
            
            try:
                with open(args.input_file) as input_file:
                    parse(input_file, output_generator)
            except Exception as e:
                logging.error(f"Unable to read input file {args.input_file}")
                exit(1)

    except Exception as e:
        logging.error(f"Unable to write to output file {args.output_file}")
        exit(1)
    

