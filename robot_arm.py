"""Class to control robot arm."""
import os
import time
import logging


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


if os.uname().nodename == "raspberrypi":
    from adafruit_servokit import ServoKit
else:
    from dummy_servo import ServoKit


class Joint:
    """Robot arm joint."""

    def __init__(self, servo, init=90, min=0, max=180):
        """Robot arm joint init.

        servo (adafruit_motor.servo.Servo): Servo class for robot arm joint
        init (int): Initial angle for servo to be set to
        min (int): Minimum angle that servo can reach
        max (int): Maximum angle that servo can reach
        """
        self.servo = servo
        self.init = init
        self.servo.angle = self.init
        self.min = min
        self.max = max
        self._increment_angle = 1
        self._valid_diff = 0.5
    
    @property
    def angle(self):
        """Get servo's current angle."""
        return self.servo.angle
    
    @angle.setter
    def angle(self, new_angle):
        """Set servo's current angle.

        new_angle (float): Angle for servo to be set to
        """
        # check if angle is out of range for joint
        if new_angle < self.min:
            new_angle = self.min
        if new_angle > self.max:
            new_angle = self.max
        self.servo.angle = new_angle

    def move(self, angle, speed=10):
        """Move robot arm joint.

        angle (float): Angle to move joint to
        speed (int): Speed to move joint at (range 1-10)
        """
        if abs(self.angle - angle) < self._valid_diff:
            return
        # handle speed out of range
        if speed > 10:
            logging.warning("speed must be in range 1 - 10")
            speed = 10
        if speed < 1:
            logging.warning("speed must be in range 1 - 10")
            speed = 1
        logging.info(f"Moving {self} from {self.angle} to {angle} with speed {speed}")
        # check if angle is out of range for joint
        if angle < self.min:
            logging.warning(f"Angle less than min selected, min: {self.min}, angle: {angle}")
            angle = self.min
        if angle > self.max:
            logging.warning(f"Angle greater than max selected, max: {self.max}, angle: {angle}")
            angle = self.max
        # speed of 10 should move instantly
        if speed == 10:
            self.angle = angle
            return
        # increment angle over period of time
        while self.angle != angle:
            logging.debug(f"current angle: {self.angle}")
            if abs(self.angle - angle) < self._valid_diff:
                self.angle = angle
                break
            if self.angle > angle:
                self.angle -= self._increment_angle
            else:
                self.angle += self._increment_angle
            time.sleep(0.05/speed)


class RobotArm:
    """Robot arm class."""

    def __init__(self):
        """Initialize robot arm."""
        self.kit = ServoKit(channels=16)
        self.servo = self.kit.servo
        self.base = Joint(self.servo[0])
        self.shoulder = Joint(self.servo[1])
        self.elbow = Joint(self.servo[2])
        self.wrist = Joint(self.servo[3])
        self.claw = Joint(self.servo[4], min=90)
        self.wrist_rotate = Joint(self.servo[5])
