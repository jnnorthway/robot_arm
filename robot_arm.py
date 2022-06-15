import os
import time


if os.uname().nodename == "raspberrypi":
    from adafruit_servokit import ServoKit
else:
    from dummy_servo import ServoKit


class Joint:

    def __init__(self, servo, min=0, max=180):
        self.servo = servo
        self.min = min
        self.max = max
    
    @property
    def angle(self):
        return self.servo.angle
    
    @angle.setter
    def angle(self, new_angle):
        self.servo.angle = new_angle


class RobotArm:

    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.servo = self.kit.servo
        self.base = Joint(self.servo[0])
        self.shoulder = Joint(self.servo[1])
        self.elbow = Joint(self.servo[2])
        self.wrist = Joint(self.servo[3])
        self.claw = Joint(self.servo[4], min=90)
        self.wrist_rotate = Joint(self.servo[5])
        self._increment_angle = 1
        self._valid_diff = 0.5
    
    def move(self, joint, angle, speed=10):
        print(f"Moving {joint} from {joint.angle} to {angle} with speed {speed}")
        if angle < joint.min:
            print("Min angle selected")
            angle = joint.min
        if angle > joint.max:
            print("Max angle selected")
            angle = joint.max
        if speed == 10:
            joint.angle = angle
            return
        while joint.angle != angle:
            print(f"current angle: {joint.angle}")
            if abs(joint.angle - angle) < self._valid_diff:
                joint.angle = angle
                break
            if joint.angle > angle:
                joint.angle -= self._increment_angle
            else:
                joint.angle += self._increment_angle
            time.sleep(0.2/speed)
