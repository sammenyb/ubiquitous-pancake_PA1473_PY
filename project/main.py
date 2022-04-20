#!/usr/bin/env pybricks-micropython
from msilib import sequence
import sys

# from project import __init__
# from project import pick_up as pu



# from pybricks.pupdevices import ForceSensor
import time
from statistics import mean as avg
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

#globala variablar
speed = 0
angle = 0
rotate_cw = True
rotation_swap_timer_max = 0
rotation_swap_timer = 0


def identify_color(rgb): #do not use this function on people or we'll get sued
    print(rgb)
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if sum(rgb) < 10:
        return "black"
    elif green >= 0.75 * red and red >= 0.75 * green and blue < 0.2 * (red + green):
        return "yellow"
    elif red >= 0.75 * blue and blue >= 0.75 * red and green < 0.2 * (red + blue):
        return "purple"
    elif green > 0.25 * red and green < 0.75 * red and blue < 0.25 * red:
        return "brown"
    elif red > 2 * (green + blue): # ORDER MATTERS! This should remain *after* checking for brown.
        return "red"
    elif green > 2 * (red + blue):
        return "green"
    elif blue > 2 * (red + green):
        return "blue"
    else:
        return "unknown"


def CollisionAvoidance():
    vehicle_detected = False
    if ultra_sensor.distance() < 150:
        vehicle_detected = True  #initialize avoid sequence
    
    if vehicle_detected:
        robot.turn(20)
        robot.straight(200)
        robot.turn(-40)
        robot.straight(200)
        robot.turn(20) 
        #look for line again
    
    return


def follow_line(colors):
    global angle, speed, rotate_cw, rotation_swap_timer_max, rotation_swap_timer
    continue_driving = 0 # does this need to be an int?

    while continue_driving == 0:
        robot.drive(speed, angle)
        color_left = left_light.rgb()
        CollisionAvoidance()

        if identify_color(color_left) in colors:
            # check if right color is the correct next color here?
            rotation_swap_timer_max = 5
            rotation_swap_timer = rotation_swap_timer_max
            angle = 0
            speed = 50
        else:
            rotation_swap_timer -= 1
            if rotation_swap_timer < 0:
                rotate_cw = not rotate_cw
                rotation_swap_timer_max += 5
                rotation_swap_timer = rotation_swap_timer_max
            if rotate_cw:
                robot.turn(2)
            else:
                robot.turn(-2)
            


        # if avg([60,60,60]) < avg(left_light.rgb()) <= avg([100,100,100]): #vit
        #     speed = 50
        #     angle = -20
        # elif avg([40,40,40]) <= avg(left_light.rgb()) <= avg([60,60,60]): #mellan svart och vit
        #     speed = 100
        #     angle = 0
        # elif avg([0,0,0]) <= avg(left_light.rgb()) < avg([40,40,40]): #svart
        #     speed = 50
        #     angle = 20
        # elif left_light.rgb == 0: #designatet vÃ¤rde   #??
        #     speed = 20
        #     angle = 90

        # else:
        #     continue_driving = 1


        

def main():
    
        loop_continue = 0

        while loop_continue == 0:
            """ihuiedhcid"""
            follow_line()


if __name__ == '__main__':
    sys.exit(main())