import unittest
from outputgenerator import MockGenerator
from nem12parser import NEM12Parser

class NEM12ParserTest(unittest.TestCase):
    def setUp(self):
        self.generator = MockGenerator()
        self.parser = NEM12Parser(self.generator, "", "", "")

    def tearDown(self):
        self.parser = None

    def test_parse_empty_file_should_generate_nothing(self):
        with open('test/empty.csv') as f:
            self.parser.parse(f)
            self.assertEqual(self.generator.generated_intervals, 0)

    def test_parse_no_200_before_300_should_raise_importerror(self):
        with open('test/missing200.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)

    def test_parse_date_non_sequential_should_raise_importerror(self):
        with open('test/nonsequentialdate.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)

    def test_parse_invalid_intervals_should_raise_importerror(self):
        with open('test/invalidintervals1.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)
        with open('test/invalidintervals2.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)
    
    def test_parse_invalid_nmi_value_should_raise_importerror(self):
        with open('test/invalidnmi.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)
        with open('test/invalidnmisuffix.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)

    def test_parse_invalid_interval_value_should_raise_importerror(self):
        with open('test/invalidintervalvalue1.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)
        with open('test/invalidintervalvalue2.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)
        with open('test/invalidintervalvalue3.csv') as f:
            with self.assertRaises(ImportError):
                self.parser.parse(f)

if __name__ == '__main__':
    unittest.main()
