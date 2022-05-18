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
    # reference_rgb = {"red_pink": (46, 17, 27), "olive_green": (15, 15, 9), "purple": (12, 10, 35), "blue": (10, 20, 33), "lime_green": (8, 27, 14)}

    reference_rgb = {"black": (4, 5, 2),  # zeroes are NOT allowed in the values of this list.
    "brown": (10, 6, 4),
    "purple": (8, 9, 20),
    "purple.2": (12, 7, 37),
    "yellow": (42, 36, 4),
    "pink_red": (36, 16, 13),
    "pink_red.2": (30, 15, 20),
    "olive_green": (12, 15, 4),
    "olive_green.2": (10, 15, 9),
    "lime_green": (8, 30, 8),
    "blue": (8, 19, 22)}

    with open('colors.json', 'w') as f:
        json.dump(reference_rgb, f)


def main():
    cal_color()
    # skriv()
if __name__ == '__main__':
    sys.exit(main())