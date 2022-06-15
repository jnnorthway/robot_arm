from robot_arm import RobotArm


def run():
    print("Running Robot Arm!")
    robot = RobotArm()
    print(f"Base angle = {robot.claw.angle}")
    robot.move(robot.claw, 180, 5)
    print(f"Base angle = {robot.claw.angle}")
    robot.move(robot.claw, 45, 7)
    print(f"Base angle = {robot.claw.angle}")

if __name__ == "__main__":
    run()
