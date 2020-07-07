from os import listdir, getenv, getcwd, chdir
from enterance_rules import enteranceRules
from os.path import isfile, join
from sqlite_db import sqlite_db
from dotenv import load_dotenv
import datetime
import requests
import Logger
import json
import time

load_dotenv()

class ocr_plate_scanner():
    def __init__(self, database, input, output, log):
        self.start = time.time()
        self.logger = Logger.init_logger(log)
        self.plate_db = sqlite_db(database, self.logger)
        self.image_files = self.get_files(input)
        self.output = output
        self.handled_plates = 0
        self.broken_files = 0
        self.allowed_formats = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

        self.logger.error("Execution started")
        self.logger.error("Initializing...\n")

    def get_files(self, folder_name):
        try:
            chdir(folder_name)
            path = getcwd()
            return [f for f in listdir(path) if isfile(join(path, f))]
        except FileNotFoundError as e:
            print(f"There is no dir named: {folder_name}, please check the name and try again.")
            exit()

    def run(self):
        for file in self.image_files:
            if file.endswith(self.allowed_formats):
                print(f"Checking plate in file: {file}")
                self.scan_and_handle_plate(file)
            else:
                self.broken_files+=1
                continue

        # Verify all decisions were recorded properly
        print()
        print("Verification:")
        print("=============")
        self.plate_db.view_db()

        end_time = time.time()
        total_time = end_time - self.start
        self.logger.error(f"\nExecution finished")
        self.logger.error(f"Handled {self.handled_plates} plates")
        self.logger.error(f"Handled {self.broken_files} Broken files")
        self.logger.error(f"Execution took: --- {total_time} seconds ---\n")

    def scan_and_handle_plate(self, image):
        test_file = self.scan_image(filename=image)
        results_dict = json.loads(test_file)

        if (results_dict["OCRExitCode"] == 99 and
                "Image size is too small for OCR Engine 2" in str(results_dict["ErrorMessage"])):
            test_file = self.scan_image(filename=image, engine=1)
            results_dict = json.loads(test_file)

        self.logger.info(results_dict)

        plate = self.extract_plate_from_text(results_dict)
        self.logger.info("Treating plate: " + str(plate) + " In File: " + str(image))

        self.handle_plate(plate)

    def scan_image(self, filename, overlay=True, language='eng', engine=2):
        payload = {'isOverlayRequired': overlay,
                   'apikey': getenv("ACCESS_TOKEN"),
                   'language': language,
                   'OCREngine': engine}

        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload)
        return r.content.decode()

    def extract_plate_from_text(self, text_dict):
        results = text_dict['ParsedResults'][0]
        text_overlay = results['TextOverlay']
        lines = text_overlay['Lines']

        max_line_height = -1    # Base Case for search
        max_line_idx = -1       # Base Case for search

        for i, line in enumerate(lines):
            if line["MaxHeight"] >= max_line_height:
                max_line_idx = i
                max_line_height = line["MaxHeight"]

        max_line = lines[max_line_idx]
        max_line_text = max_line["LineText"]

        return max_line_text

    def handle_plate(self, plate):

        allowed=True
        decision_cause = ""
        amt_of_digits = enteranceRules.count_digits(plate)
        sum_of_digits = enteranceRules.sum_digits(plate)

        self.logger.warning("DIGITS IN PLATE IS: " + str(enteranceRules.count_digits(plate)))
        self.logger.warning("SUM OF PLATE IS: " + str(enteranceRules.sum_digits(plate)))
        self.logger.warning("LAST DIGITS ARE 25|26: " + str(enteranceRules.check_last_digits(1, plate)))
        self.logger.warning("LAST DIGITS ARE 85|86|87|88|89|00: " + str(enteranceRules.check_last_digits(2, plate)))
        self.logger.warning("Is emergency vehicle?: " + str(enteranceRules.check_emergency_vehicles(plate)))

        # 1st case - Vehicles with emergency plate numbers aren't allowed to enter.
        if enteranceRules.check_emergency_vehicles(plate):
            allowed = False
            decision_cause = "emergency"

        # 2nd case - Vehicles with public transportation plate numbers with specific
        # last 2 digits aren't allowed to enter.
        elif enteranceRules.check_last_digits(1, plate):
            allowed = False
            decision_cause = "public"

        # 3rd case - Vehicles with 7 Digits plate numbers with specific last 2 digits
        # aren't allowed to enter.
        elif amt_of_digits == 7 and enteranceRules.check_last_digits(2, plate):
            allowed = False
            decision_cause = "7-digit"

        # 4th case - Vehicles with 7 or 8 digits plate number in which the sum of all
        # digits is divisible by 7 without residue aren't allowed to enter.
        elif ((amt_of_digits == 7 or amt_of_digits == 8 ) and (sum_of_digits % 7 == 0)):
            allowed = False
            decision_cause = "7-8-digit"

        # All other plate numbers are allowed to enter.
        else:
            decision_cause = "allowed"

        now = datetime.datetime.now()
        datestring = now.strftime("%Y-%m-%d %H:%M:%S")
        decided = "1" if allowed else "0"
        decision = (plate, decision_cause, datestring, decided)
        self.plate_db.add_vehicle_to_db(decision)
        self.handled_plates += 1

        self.logger.error(decision)