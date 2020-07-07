import Args_parser
from OCR_plate_reader import ocr_plate_scanner

__title__ = 'Python Plate Scanner'
__version__ = '0.1.1 Alpha'
__author__ = 'Arie Charfnadel'
__license__ = 'GPLv3'
__url__ = 'https://github.com/LevChar/Python-Plate-Scanner'

if __name__ == "__main__":
    scanner = ocr_plate_scanner(**Args_parser.args_parser())
    scanner.run()