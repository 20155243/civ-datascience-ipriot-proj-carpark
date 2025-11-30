from smartpark.interfaces import CarparkSensorListener
from smartpark.interfaces import CarparkDataProvider
from smartpark.config_parser import parse_config
import time
import os

'''
    TODO: 
    - Read your configuration from a file. 
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature

'''


class CarparkManager(CarparkSensorListener, CarparkDataProvider):
    # constant, for where to get the configuration data
    CONFIG_FILE = "config.json"
    LOG_FILE = "carpark_log.txt"

    def __init__(self):
        self.config = parse_config(CarparkManager.CONFIG_FILE)
        self.total_spaces = self.config.get("total-spaces", 100)
        print("Total spaces:", self.total_spaces)
        self.available_spaces = self.total_spaces
        self.temperature = 20
        self.current_time = time.localtime()

        # Track cars
        self.cars = {}  # dict of license_plate -> Car object

        # Display reference (set externally)
        self.display = None

        # Ensure log file exists
        if not os.path.exists(CarparkManager.LOG_FILE):
            with open(CarparkManager.LOG_FILE, "w") as f:
                f.write("Carpark Log Started\n")

        # ---------------- Logging ----------------

    def log_event(self, message: str):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(CarparkManager.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)  # also print to console

    # ---------------- Data Provider ----------------

    @property
    def available_spaces(self):
        return self._available_spaces

    @available_spaces.setter
    def available_spaces(self, value):
        self._available_spaces = value

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def current_time(self):
        return time.localtime()

    @current_time.setter
    def current_time(self, value):
        self._current_time = value

    def incoming_car(self, license_plate):
        # print('Car in! ' + license_plate)
        if self.available_spaces > 0:
            car = Car(license_plate)
            self.entry_time = time.localtime()
            self.cars[license_plate] = car
            self.available_spaces -= 1
            self.log_event(f"Car entered: {license_plate}, spaces left: {self.available_spaces}")
        else:
            self.log_event("Carpark full! Entry denied.")

            # Trigger display update
        if self.display:
            self.display.update_event.set()

    def outgoing_car(self, license_plate):
        # print('Car out! ' + license_plate)
        car = self.cars.get(license_plate)
        if car:
            self.exit_time = time.localtime()
            self.available_spaces += 1
            self.log_event(f"Car exited: {license_plate}, spaces left: {self.available_spaces}")
        else:
            self.log_event(f"Unknown car tried to exit: {license_plate}")

        if self.display:
            self.display.update_event.set()

    def temperature_reading(self, reading):
        # print(f'temperature is {reading}')
        self.temperature = reading
        self.log_event(f"Temperature updated: {reading}℃")

        if self.display:
            self.display.update_event.set()


class Car:
    def __init__(self, plate=None):
        self.LicensePlate = plate
        self.entry_time = None
        self.exit_time = None