"""Script to run robot arm."""
from robot_arm import RobotArm
import logging
import PySimpleGUIWeb as sg


def get_joint_col(name, joint, reverse=False):
    """Create column for joint control."""
    joint_name = name.lower().replace(" ", "_")
    slider = sg.Slider((joint.min, joint.max), orientation="h", default_value=joint.angle, key=joint_name, enable_events=True)
    return sg.Column(
        [
            [sg.Text(name)],
            [slider],
        ]
    )


def do_move(robot, values):
    """Move joint based on dictionary values."""
    base_val = float(values.get("base", None))
    shoulder_val = float(values.get("shoulder", None))
    elbow_val = float(values.get("elbow", None))
    wrist_val = float(values.get("wrist", None))
    wrist_rot_val = float(values.get("wrist_rotation", None))
    claw_val = float(values.get("claw", None))
    robot.base.move(base_val)
    robot.shoulder.move(shoulder_val)
    robot.elbow.move(elbow_val)
    robot.wrist.move(wrist_val)
    robot.wrist_rotate.move(wrist_rot_val)
    robot.claw.move(claw_val)


def update_slider(col, val):
    """Update slider in column."""
    col.Rows[1][0].update(value=val)


def run():
    """Run robot arm"""
    logging.info("Running Robot Arm!")
    robot = RobotArm()
    base_col = get_joint_col("Base", robot.base)
    shoulder_col = get_joint_col("Shoulder", robot.shoulder)
    elbow_col = get_joint_col("Elbow", robot.elbow, reverse=True)
    wrist_col = get_joint_col("Wrist", robot.wrist)
    wrist_rot_col = get_joint_col("Wrist Rotation", robot.wrist_rotate)
    claw = get_joint_col("Claw", robot.claw)

    base_col.AddRow(wrist_col)
    shoulder_col.AddRow(wrist_rot_col)
    elbow_col.AddRow(claw)

    sleep_btn = sg.Button(
        "Sleep", key="sleep_btn"
    )
    quit_btn = sg.Button(
        "Quit", key="quit_btn"
    )

    layout = [
        [sg.Text("Robot Arm Controller")],
        [base_col, shoulder_col, elbow_col],
        [sleep_btn, quit_btn]
    ]
    window = sg.Window("Robot Arm Controller", layout, web_port=30000)
    while True:
        try:
            event, values = window.read()
            logging.debug(f"event: {event}, values {values}")
            if event in ("sleep_btn", "quit_btn"):
                robot.sleep()
                update_slider(base_col, robot.base.angle)
                update_slider(shoulder_col, robot.shoulder.angle)
                update_slider(elbow_col, robot.elbow.angle)
                update_slider(wrist_col, robot.wrist.angle)
                update_slider(wrist_rot_col, robot.wrist_rotate.angle)
                update_slider(claw, robot.claw.angle)
            if event == "sleep_btn":
                continue
            if event in (sg.WINDOW_CLOSED, "quit_btn"):
                break
            do_move(robot, values)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Failed to read event: {e}")

    window.close()


if __name__ == "__main__":
    run()
