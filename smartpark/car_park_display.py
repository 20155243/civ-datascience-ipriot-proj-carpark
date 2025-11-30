from interfaces import CarparkDataProvider
import threading
import time
import tkinter as tk
from typing import Iterable


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, root, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Toplevel(root)
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):
            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field + self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""

    #        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()


# -----------------------------------------#
# TODO: STUDENT IMPLEMENTATION STARTS HERE #
# -----------------------------------------#

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self, root):
        self.window = WindowedDisplay(root,'Moondalup', CarParkDisplay.fields)

        self.update_event = threading.Event()  # Event Signal defined

        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()

        self.window.show()
        self._provider = None



    @property
    def data_provider(self):
        return self._provider

    @data_provider.setter
    def data_provider(self, provider):
        if isinstance(provider, CarparkDataProvider):
            self._provider = provider

    def update_display(self):
        field_values = dict(zip(CarParkDisplay.fields, [
            f'{self._provider.available_spaces:03d}',
            f'{self._provider.temperature:.1f}℃',
            time.strftime("%H:%M:%S", self._provider.current_time)
        ]))
        self.window.update(field_values)

    def check_updates(self):
        while True:
            # TODO: This timer is pretty janky! Can you provide some kind of signal from your code
            # to update the display?
            #time.sleep(1)
            self.update_event.wait()  # Waits for Update Signal
            self.update_event.clear()
            # When you get an update, refresh the display.
            if self._provider is not None:
                self.update_display()
