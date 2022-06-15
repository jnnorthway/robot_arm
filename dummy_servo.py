
class Servo:

    def __init__(self):
        self.angle = 90
        self.actuation_range = 180
    
    def set_pulse_width_range(self, low, high):
        print(f"Setting pulse width range to: {low}, {high}")

class ServoKit:

    def __init__(self, channels):
        self.channels = channels
        self.servo = []
        for _ in range(self.channels):
            self.servo.append(Servo())
