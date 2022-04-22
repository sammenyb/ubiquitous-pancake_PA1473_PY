#!/usr/bin/env pybricks-micropython
import sys


# from project import __init__
# from project import pick_up as pu



# from pybricks.pupdevices import ForceSensor
import time
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
left_light = ColorSensor(Port.S3)

def identify_color(rgb): #do not use this function on people or we'll get sued
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if sum(rgb) < 10:
        return Color.BLACK
    elif green >= 0.6 * red and red >= 0.8 * green and blue < 0.3 * (red + green):
        return Color.YELLOW
    elif red >= 0.75 * blue and blue >= 0.75 * red and green < 0.2 * (red + blue):
        return Color.PURPLE
    elif green > 0.25 * red and green < 0.6 * red and blue < 0.25 * red:
        return Color.BROWN
    elif red > 1.6 * (green + blue): # ORDER MATTERS! This should remain *after* checking for brown.
        return Color.RED
    elif green > 1.6 * red + 1.2 * blue:
        return Color.GREEN
    elif blue > 1.26 * red + 0.82 * green:
        return Color.BLUE
    else:
        return Color.WHITE

fortsatt = 0
while fortsatt == 0:
    wait(400)
    farg = left_light.rgb()
    print("color rgb: " + str(farg) + ", current color: " + str(identify_color(farg)) + ", built-in detection of color: " + str(left_light.color()))

