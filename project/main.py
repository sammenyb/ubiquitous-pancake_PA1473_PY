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
route = []


def identify_color(rgb): #do not use this function on people or we'll get sued
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if sum(rgb) < 10:
        return Color.BLACK
    elif green >= 0.75 * red and red >= 0.75 * green and blue < 0.2 * (red + green):
        return Color.YELLOW
    elif red >= 0.75 * blue and blue >= 0.75 * red and green < 0.2 * (red + blue):
        return Color.PURPLE
    elif green > 0.25 * red and green < 0.6 * red and blue < 0.25 * red:
        return Color.BROWN
    elif red > 1.5 * (green + blue): # ORDER MATTERS! This should remain *after* checking for brown.
        return Color.RED
    elif green > 1.9 * red + 1.3 * blue:
        return Color.GREEN
    elif blue > 1.6 * red + 1.0 * green:
        return Color.BLUE
    else:
        return Color.WHITE

def robot_status(status):
    print("The robot is " + str(status) + "right now")

def feedback(color,beep_duration, beep_frequency):
    
    speaker.beep(beep_frequency, beep_duration)
    light.on(color)
    return

def avg(list_of_stuff):
    return sum(list_of_stuff) / len(list_of_stuff)


def collision_avoidance():
    robot_status(status="avoiding collision")
    
    vehicle_detected = False
    if ultra_sensor.distance() < 200:
        vehicle_detected = True  #initialize avoid sequence

    if vehicle_detected: #vehicle wheels rotate the wrong way
        robot.turn(-70)
        robot.straight(-200)
        robot.turn(90)
        robot.straight(-300)
    

    return

'''def color_prio(current_prio):
    current_color = left_light.color()
    route.append(current_color)
    # fortsätt till $pickup hittad
    pick_up = input("pickup point?: ")
    drop_off = input("drop off point?: ")
   
'''



def angle_change(rgb_value):
    if rgb_value > 15:
        return rgb_value/15
    else:
        return 40/(rgb_value + 1) #no division by zero



def follow_line(colors):
    robot_status(status="following " + str(left_light.color()) + " line")
    global angle, speed, rotate_cw, rotation_swap_timer_max, rotation_swap_timer
    continue_driving = 0 # does this need to be an int?
    while continue_driving == 0:
        collision_avoidance()
        color_left = left_light.rgb()
        turnrate = angle_change(avg(color_left))
        robot.drive(- (min(8 + speed*(3/turnrate), 70)), angle*turnrate)
        current_color = identify_color(color_left)
        print("current color: " + str(current_color) + ", built-in detection of color: " + str(left_light.color()) + ", color rgb: " + str(color_left))


        color_multiplier = 1
        if current_color == Color.YELLOW:
            color_multiplier = 0.24

        if len(colors) > 1 and current_color == colors[1]:
            colors.pop(0)
            robot.straight(120) #backwards
            robot.turn(230) #turn doesn't work quite properly so this ain't degrees
        elif 23 < avg(left_light.rgb()) * color_multiplier <= 100 and current_color != colors[0]:
            speed = 40
            angle = -10
        elif 14 <= avg(left_light.rgb()) * color_multiplier <= 23 and current_color != colors[0]:
            speed = 70
            angle = 0
        else:
            speed = 40
            angle = 10

        
        route.append(current_color)
        #print("route: " + str(route))
        print("speed " + str(speed) + ", angle " + str(angle))

def reports(instructions):
    print('instructions that will be performed: ', instructions)

def cranelift():
    print("motor angle " + str(crane_motor.angle()))
    crane_motor.run_angle(15, -60, wait=True)
    # crane_motor.run_angle(15, 60, wait=True)

def main():
    instructions = [Color.BLUE, Color.YELLOW, Color.BLUE]
    loop_continue = 0
    #cranelift()
    reports(instructions)
    while loop_continue == 0:
        """ihuiedhcid()"""
        follow_line(instructions) #"yellow", "brown", "green", "blue", "red"
        



if __name__ == '__main__':
    sys.exit(main())