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


def robot_status(status):
    print("The robot is " + str(status) + "right now")

def avg(list_of_stuff):
    return sum(list_of_stuff) / len(list_of_stuff)




def collision_avoidance():
    robot_status(status="avoiding collision")
    
    vehicle_detected = False
    if ultra_sensor.distance() < 200:
        vehicle_detected = True  #initialize avoid sequence

    if vehicle_detected: #vehicle wheels rotate the wrong way
        robot.turn(-20)
        robot.straight(-200)
        robot.turn(40)
        robot.straight(-200)
    

    return
#def color_prio(current_prio):

def angle_change(rgb_value):
    return rgb_value/12



def follow_line(colors):
    robot_status(status="following line")
    global angle, speed, rotate_cw, rotation_swap_timer_max, rotation_swap_timer
    continue_driving = 0 # does this need to be an int?
    while continue_driving == 0:
        collision_avoidance()
        color_left = left_light.rgb()
        turnrate = angle_change(avg(color_left))
        robot.drive(- (min(speed*(1/turnrate), 80)), angle*turnrate)
        current_color = left_light.color()

        # if identify_color(color_left) in colors:
        #     # check if right color is the correct next color here?
        #     rotation_swap_timer_max = 5
        #     rotation_swap_timer = rotation_swap_timer_max
        #     angle = 0
        #     speed = 50
        # else:
        #     rotation_swap_timer -= 1
        #     if rotation_swap_timer < 0:
        #         rotate_cw = not rotate_cw
        #         rotation_swap_timer_max += 5
        #         rotation_swap_timer = rotation_swap_timer_max
        #     if rotate_cw:
        #         robot.turn(2)
        #     else:
        #         robot.turn(-2)
        
        if len(colors) > 1 and current_color == colors[1]:
            colors.pop(0)

        color_multiplier = 1
        if current_color == Color.YELLOW:
            color_multiplier = 0.4

        if 20 < avg(left_light.rgb()) * color_multiplier <= 100 and current_color != colors[0]: #vit
            speed = 40
            angle = -10
        elif 10 <= avg(left_light.rgb()) * color_multiplier <= 20 and current_color != colors[0]: #mellan svart och vit
            speed = 70
            angle = 0
        else: #svart
            speed = 40
            angle = 10

        
        
        print("speed " + str(speed) + ", angle " + str(angle) + ", color rgb: " + str(color_left) + " = " + str(current_color))

def reports(instructions):
    print('instructions that will be performed: ', instructions)

def cranelift():
    print("motor angle " + str(crane_motor.angle()))
    crane_motor.run_angle(15, -60, wait=True)
    crane_motor.run_angle(15, 60, wait=True)

def main():
    instructions = [Color.BLUE, Color.YELLOW, Color.BLUE]
    loop_continue = 0
    #cranelift()
    reports(instructions)
    while loop_continue == 0:
        """ihuiedhcid"""
        follow_line(instructions) #"yellow", "brown", "green", "blue", "red"
        collision_avoidance()


if __name__ == '__main__':
    sys.exit(main())