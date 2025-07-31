from pymavlink import mavutil

zephyr = mavutil.mavlink_connection('/devserial0', baud=115200)

def send_rc_override(roll=1500, pitch=1500, throttle=1000, yaw=1500):
    """
    Send RC override command.
    roll, pitch, throttle, yaw: PWM values (1000-2000)
    """
    zephyr.mav.rc_channels_override_send(
        zephyr.target_system,
        zephyr.target_component,
        roll,    # RC1
        pitch,   # RC2
        throttle,# RC3
        yaw,     # RC4
        0, 0, 0, 0  # RC5-RC8
    )

def move_forward():
    send_rc_override(pitch=1600)

def move_backward():
    send_rc_override(pitch=1400)

def move_left():
    send_rc_override(roll=1400)

def move_right():
    send_rc_override(roll=1600)

def stop():
    send_rc_override()