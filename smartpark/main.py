"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.

You need to split the classes here into two files, one for the CarParkDisplay and one for the CarDetector.
Attend to the TODOs in each class to complete the implementation."""
from interfaces import CarparkSensorListener
import tkinter as tk
#TODO: replace this module with yours
from carpark import CarparkManager
from car_park_display import CarParkDisplay
from car_detector import CarDetectorWindow


if __name__ == '__main__':
    root = tk.Tk()

    #TODO: This is my dodgy mockup. Replace it with a good one!
    manager = CarparkManager()

    display = CarParkDisplay(root)
    #TODO: Set the display to use your data source

    display.data_provider = manager
    manager.display = display

    detector=CarDetectorWindow(root)
    #TODO: Attach your event listener
    detector.add_listener(manager)

    root.mainloop()
