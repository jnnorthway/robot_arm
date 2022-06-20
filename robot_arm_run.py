"""Script to run robot arm."""
from email.mime import base
from robot_arm import RobotArm
import logging
import PySimpleGUIWeb as sg 
# import PySimpleGUI as sg


def get_col(name, joint):
    joint_name = name.lower().replace(" ", "_")
    # return sg.Column(
    #     [
    #         [sg.Push(), sg.Text(name), sg.Push()],
    #         [sg.Push(), sg.Slider((joint.min, joint.max), orientation="h", default_value=joint.angle, key=joint_name, enable_events=True), sg.Push()],
    #     ]
    # )
    return sg.Column(
        [
            [sg.Text(name)],
            [sg.Slider((joint.min, joint.max), orientation="h", default_value=joint.angle, key=joint_name, enable_events=True)],
        ]
    )


def do_move(robot, values):
    base_val = float(values.get("base", None))
    shoulder_val = float(values.get("shoulder", None))
    elbow_val = float(values.get("elbow", None))
    wrist_val = float(values.get("wrist", None))
    wrist_rot_val = float(values.get("wrist_rotation", None))
    claw_val = float(values.get("claw", None))
    robot.base.move(base_val, speed=9)
    robot.shoulder.move(shoulder_val, speed=9)
    robot.elbow.move(elbow_val, speed=9)
    robot.wrist.move(wrist_val, speed=9)
    robot.wrist_rotate.move(wrist_rot_val, speed=9)
    robot.claw.move(claw_val, speed=9)


def run():
    """Run robot arm"""
    logging.info("Running Robot Arm!")
    robot = RobotArm()
    base_col = get_col("Base", robot.base)
    shoulder_col = get_col("Shoulder", robot.shoulder)
    elbow_col = get_col("Elbow", robot.elbow)
    wrist_col = get_col("Wrist", robot.wrist)
    wrist_rot_col = get_col("Wrist Rotation", robot.wrist_rotate)
    claw = get_col("Claw", robot.claw)

    base_col.AddRow(wrist_col)
    shoulder_col.AddRow(wrist_rot_col)
    elbow_col.AddRow(claw)

    # layout = [
    #     [sg.Push(), sg.Text("Robot Arm Controller"), sg.Push()],
    #     [sg.Push(), base_col, shoulder_col, elbow_col, sg.Push()],
    # ]
    layout = [
        [sg.Text("Robot Arm Controller")],
        [base_col, shoulder_col, elbow_col],
    ]
    window = sg.Window("Robot Arm Controller", layout, web_port=30000)
    while True:
        try:
            event, values = window.read()
            logging.debug(f"event: {event}, values {values}")
            if event == sg.WINDOW_CLOSED:
                break
            do_move(robot, values)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Failed to read event: {e}")

    window.close()


if __name__ == "__main__":
    run()
