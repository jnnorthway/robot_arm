"""Script to run robot arm."""
from robot_arm import RobotArm
import logging


def run():
    """Run robot arm"""
    logging.info("Running Robot Arm!")
    robot = RobotArm()
    logging.info(f"Base angle = {robot.claw.angle}")
    robot.move(robot.claw, 180, 9)
    logging.info(f"Base angle = {robot.claw.angle}")
    robot.move(robot.claw, 45, 9)
    logging.info(f"Base angle = {robot.claw.angle}")


if __name__ == "__main__":
    run()
