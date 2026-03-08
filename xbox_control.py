#!/usr/bin/env python3
"""Control two SO101 arms with Xbox controller - LB to switch arms"""

import evdev
import select
import json
import time
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors.motors_bus import Motor, MotorCalibration, MotorNormMode

# Bras 1 (gauche) = 6 moteurs, Bras 2 (droit) = 4 moteurs
PORT_BRAS1 = '/dev/ttyACM3'
PORT_BRAS2 = '/dev/ttyACM2'
CALIB_PATH = '/home/zarax/.cache/huggingface/lerobot/calibration/robots/so_follower/zarax.json'
SPEED = 2.0
DEADZONE = 8000
LOOP_HZ = 30

REST_POSITION_BRAS1 = {
    'shoulder_pan': -4.8,
    'shoulder_lift': -92.4,
    'elbow_flex': 92.8,
    'wrist_flex': 42.0,
    'wrist_roll': -50.1,
    'gripper': -38.1,
}
REST_POSITION_BRAS2 = {
    'shoulder_pan': -5.4,
    'shoulder_lift': -98.8,
    'elbow_flex': 100.0,
    'wrist_flex': 51.9,
    'wrist_roll': -3.0,
    'gripper': -77.4,
}

BRAS1_MOTORS = ['shoulder_pan', 'shoulder_lift', 'elbow_flex', 'wrist_flex', 'wrist_roll', 'gripper']
BRAS2_MOTORS = ['shoulder_pan', 'shoulder_lift', 'elbow_flex', 'wrist_flex', 'wrist_roll', 'gripper']

with open(CALIB_PATH) as f:
    calib_data = json.load(f)

def make_bus(port, motor_names):
    motors = {}
    calibration = {}
    for name in motor_names:
        data = calib_data[name]
        motors[name] = Motor(data['id'], 'sts3215', MotorNormMode.RANGE_M100_100)
        calibration[name] = MotorCalibration(
            id=data['id'], drive_mode=data['drive_mode'],
            homing_offset=data['homing_offset'],
            range_min=data['range_min'], range_max=data['range_max']
        )
    bus = FeetechMotorsBus(port=port, motors=motors, calibration=calibration)
    bus.connect()
    return bus

# Connexion des deux bras
print('Connexion bras 1 (gauche, 6 moteurs)...')
bus1 = make_bus(PORT_BRAS1, BRAS1_MOTORS)
print('Connexion bras 2 (droit, 6 moteurs)...')
bus2 = make_bus(PORT_BRAS2, BRAS2_MOTORS)

# Lire positions initiales des deux bras
positions = {
    1: {},  # bras 1
    2: {},  # bras 2
}
for name in BRAS1_MOTORS:
    positions[1][name] = bus1.read('Present_Position', name)
for name in BRAS2_MOTORS:
    positions[2][name] = bus2.read('Present_Position', name)

buses = {1: bus1, 2: bus2}
motor_lists = {1: BRAS1_MOTORS, 2: BRAS2_MOTORS}
active_arm = 1

def print_status():
    arm_name = "GAUCHE (6 moteurs)" if active_arm == 1 else "DROIT (6 moteurs)"
    print(f'\n>>> Bras actif: {active_arm} - {arm_name} <<<')

print('\n=== Xbox Control - 2 Bras ===')
print('Stick G X: shoulder_pan (1) / Stick G Y: shoulder_lift (2)')
print('Stick D Y: elbow_flex (3) / Stick D X: wrist_flex (4)')
print('LB/RB: wrist_roll (5)')
print('LT/RT: gripper (6)')
print('D-pad gauche/droit: changer de bras')
print('Y: vitesse + / X: vitesse -')
print('B: quitter')
print('=============================')
print_status()

def find_gamepad():
    for path in evdev.list_devices():
        dev = evdev.InputDevice(path)
        if 'xbox' in dev.name.lower() or 'wireless' in dev.name.lower():
            return dev
    return None

def norm(value):
    if abs(value) < DEADZONE:
        return 0.0
    return value / 32768.0

def safe_write(bus, motor_name, value):
    try:
        bus.write('Goal_Position', motor_name, value)
    except Exception:
        pass

axes = {'ABS_X': 0, 'ABS_Y': 0, 'ABS_RX': 0, 'ABS_RY': 0, 'ABS_Z': 0, 'ABS_RZ': 0, 'ABS_HAT0X': 0, 'ABS_HAT0Y': 0}
btn_lb = 0
btn_rb = 0
running = True
loop_period = 1.0 / LOOP_HZ

while running:
    gamepad = find_gamepad()
    if not gamepad:
        print('Manette non trouvee, attente...')
        time.sleep(2)
        continue

    print(f'Manette connectee: {gamepad.name}')
    try:
        while running:
            t0 = time.time()

            while True:
                r, _, _ = select.select([gamepad.fd], [], [], 0)
                if not r:
                    break
                for event in gamepad.read():
                    if event.type == evdev.ecodes.EV_ABS:
                        code_name = evdev.ecodes.ABS[event.code]
                        if code_name in axes:
                            axes[code_name] = event.value
                        if code_name == 'ABS_HAT0X':
                            if event.value == -1:
                                active_arm = 1
                                print_status()
                            elif event.value == 1:
                                active_arm = 2
                                print_status()
                    elif event.type == evdev.ecodes.EV_KEY:
                        if event.code == evdev.ecodes.BTN_B and event.value == 1:
                            running = False
                        elif event.code == evdev.ecodes.BTN_Y and event.value == 1:
                            SPEED = min(5.0, SPEED + 0.5)
                            print(f'Vitesse: {SPEED}')
                        elif event.code == evdev.ecodes.BTN_X and event.value == 1:
                            SPEED = max(0.25, SPEED - 0.5)
                            print(f'Vitesse: {SPEED}')
                        elif event.code == evdev.ecodes.BTN_TL:
                            btn_lb = event.value
                        elif event.code == evdev.ecodes.BTN_TR:
                            btn_rb = event.value

            if not running:
                break

            cur_bus = buses[active_arm]
            cur_pos = positions[active_arm]
            cur_motors = motor_lists[active_arm]

            dx = norm(axes['ABS_X'])
            dy = norm(axes['ABS_Y'])
            rx = norm(axes['ABS_RX'])
            ry = norm(axes['ABS_RY'])
            dpad_y = axes['ABS_HAT0Y']
            lt = axes['ABS_Z'] / 255.0
            rt = axes['ABS_RZ'] / 255.0

            moved = False
            if dx != 0:
                cur_pos['shoulder_pan'] = max(-100, min(100, cur_pos['shoulder_pan'] + dx * SPEED))
                moved = True
            if dy != 0:
                cur_pos['shoulder_lift'] = max(-100, min(100, cur_pos['shoulder_lift'] - dy * SPEED))
                moved = True
            if ry != 0:
                cur_pos['elbow_flex'] = max(-100, min(100, cur_pos['elbow_flex'] + ry * SPEED))
                moved = True
            if rx != 0 and 'wrist_flex' in cur_motors:
                cur_pos['wrist_flex'] = max(-100, min(100, cur_pos['wrist_flex'] + rx * SPEED))
                moved = True
            if (btn_lb or btn_rb) and 'wrist_roll' in cur_motors:
                cur_pos['wrist_roll'] = max(-100, min(100, cur_pos['wrist_roll'] + (btn_lb - btn_rb) * SPEED))
                moved = True
            if (lt > 0.1 or rt > 0.1) and 'gripper' in cur_motors:
                cur_pos['gripper'] = max(-100, min(100, cur_pos['gripper'] + (rt - lt) * SPEED))
                moved = True

            if moved:
                for name in cur_pos:
                    safe_write(cur_bus, name, cur_pos[name])

            elapsed = time.time() - t0
            sleep_time = loop_period - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except OSError:
        print('Manette deconnectee, reconnexion...')
        time.sleep(1)
    except KeyboardInterrupt:
        running = False

print('Position de repli...')
steps = 60
for i in range(1, steps + 1):
    t = i / steps
    for name in REST_POSITION_BRAS1:
        target = positions[1][name] + (REST_POSITION_BRAS1[name] - positions[1][name]) * t
        safe_write(bus1, name, target)
    for name in REST_POSITION_BRAS2:
        target = positions[2][name] + (REST_POSITION_BRAS2[name] - positions[2][name]) * t
        safe_write(bus2, name, target)
    time.sleep(1.0 / LOOP_HZ)

bus1.disconnect()
bus2.disconnect()
print('Bye!')
