"""Dummy ServoKit class for robot arm development."""
import logging


class Servo:
    """Dummy Servo class."""

    def __init__(self):
        """Initialize dummy servo."""
        self.angle = 90
        self.actuation_range = 180
    
    def set_pulse_width_range(self, min_pulse=750, max_pulse=2250):
        """Set pulse width range.

        min_pulse (int): The minimum pulse length of the servo in microseconds
        max_pulse (int): The maximum pulse length of the servo in microseconds
        """
        logging.debug(f"Setting pulse width range to: {min_pulse}, {max_pulse}")


class ServoKit:

    def __init__(self, channels):
        self.channels = channels
        self.servo = []
        for _ in range(self.channels):
            self.servo.append(Servo())
