#!/usr/bin/env pybricks-micropython
from copy import copy
# from msilib.schema import ControlCondition
import sys

# import statistics
# list_test = [3,2,1,5,5]
# print(statistics.median([3,2,5,5]))
# from project import __init__
# from project import pick_up as pu
import json


# from pybricks.pupdevices import ForceSensor
import time
# from matplotlib import lines
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.hubs import EV3Brick
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks import robotics
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.robotics import DriveBase





ev3 = EV3Brick()
# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
crane_motor = Motor(Port.A)

left_light = ColorSensor(Port.S3)

ultra_sensor = UltrasonicSensor(Port.S4)


# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=47, axle_track=128)


def cal_color():
    print('')
    reference_rgb = {}
    reference_rgb["blue"] = left_light.rgb()
    print("TRUE RGB Blue: ",left_light.rgb())

    ev3.speaker.beep()
    wait(5000)
    reference_rgb["red_pink"] = left_light.rgb()
    print("TRUE RGB Red_Pink: ",left_light.rgb())

    ev3.speaker.beep()
    wait(5000)
    reference_rgb["purple"] = left_light.rgb()
    print("TRUE RGB Purple: ",left_light.rgb())

    ev3.speaker.beep()
    wait(5000)
    reference_rgb["olive_green"] = left_light.rgb()
    print("TRUE RGB Olive_green: ",left_light.rgb())

    ev3.speaker.beep()
    wait(5000)
    reference_rgb["lime_green"] = left_light.rgb()
    print("TRUE RGB lime_green: ",left_light.rgb())

    ev3.speaker.beep()
    wait(300)
    ev3.speaker.beep()
    print('Dict',reference_rgb)


    with open('colors.json', 'w') as f:
        json.dump(reference_rgb, f)


def skriv():
    reference_rgb = {'red_pink': (62, 60, 98), 'olive_green': (62, 60, 98), 'purple': (62, 60, 98), 'blue': (62, 60, 98), 'lime_green': (62, 60, 98)}

    with open('colors.json', 'w') as f:
        json.dump(reference_rgb, f)


def main():
    cal_color()
    # skriv()
if __name__ == '__main__':
    sys.exit(main())