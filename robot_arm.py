"""Class to control robot arm."""
import os
import time
import logging
from threading import Thread, Lock


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


if os.uname().nodename == "raspberrypi":
    from adafruit_servokit import ServoKit
else:
    from dummy_servo import ServoKit


class Joint:
    """Robot arm joint."""

    def __init__(self, servo, speed=3, init_angle=90, min=0, max=180):
        """Robot arm joint init.

        servo (adafruit_motor.servo.Servo): Servo class for robot arm joint
        speed (int): Speed for servo to move
        init_angle (int): Initial angle for servo to be set to
        min (int): Minimum angle that servo can reach
        max (int): Maximum angle that servo can reach
        """
        self.servo = servo
        self.init_angle = init_angle
        self.speed = speed
        self.min = min
        self.max = max
        self._increment_angle = self.speed
        self._valid_diff = 0.5
        self.servo.angle = self.init_angle
        self.lock = Lock()
    
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
    
    def speed_move(self, angle):
        # increment angle over period of time
        self.lock.acquire()
        angle_val = self.angle
        while angle_val != angle:
            logging.debug(f"current angle: {angle_val}")
            time.sleep(0.2)
            if abs(angle_val - angle) < self._increment_angle + self._valid_diff:
                self.angle = angle
                break
            if angle_val > angle:
                self.angle -= self._increment_angle
                angle_val -= self._increment_angle
            else:
                self.angle += self._increment_angle
                angle_val += self._increment_angle
        self.lock.release()

    def move(self, angle):
        """Move robot arm joint.

        angle (float): Angle to move joint to
        speed (int): Speed to move joint at (range 1-10)
        """
        if abs(self.angle - angle) < self._valid_diff:
            return
        # handle speed out of range
        if self.speed > 10:
            logging.warning("speed must be in range 1 - 10")
            self.speed = 10
        if self.speed < 1:
            logging.warning("speed must be in range 1 - 10")
            self.speed = 1
        logging.info(f"Moving {self} from {self.angle} to {angle} with speed {self.speed}")
        # check if angle is out of range for joint
        if angle < self.min:
            logging.warning(f"Angle less than min selected, min: {self.min}, angle: {angle}")
            angle = self.min
        if angle > self.max:
            logging.warning(f"Angle greater than max selected, max: {self.max}, angle: {angle}")
            angle = self.max
        # speed of 10 should move instantly
        if self.speed == 10:
            self.angle = angle
            return
        Thread(target=self.speed_move, args=(angle,)).start()

    def sleep(self):
        """Returns joint to initial position."""
        self.move(self.init_angle)


class RobotArm:
    """Robot arm class."""

    def __init__(self):
        """Initialize robot arm."""
        self.kit = ServoKit(channels=16)
        self.servo = self.kit.servo
        self.base = Joint(self.servo[0], 3, init_angle=90)
        self.shoulder = Joint(self.servo[1], 2, init_angle=90, min=90)
        self.elbow = Joint(self.servo[2], 3, init_angle=180)
        self.wrist = Joint(self.servo[3], 3, init_angle=180) # Flip rotation
        self.claw = Joint(self.servo[4], 3, init_angle=90, min=90)
        self.wrist_rotate = Joint(self.servo[5], 3, init_angle=0)
        self.joints = {
            "base": self.base,
            "shoulder": self.shoulder,
            "elbow": self.elbow,
            "wrist": self.wrist,
            "wrist_rotate": self.wrist_rotate,
            "claw": self.claw,
        }
    
    def sleep(self):
        """Returns robot arm to initial position."""
        logging.info("Setting robot into sleep position")
        for joint in self.joints.values():
            joint.sleep()


