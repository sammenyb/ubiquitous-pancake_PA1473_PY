#!/usr/bin/env pybricks-micropython
from copy import copy
# from msilib.schema import ControlCondition
import sys

import csv


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

#globala variablar
speed = 0
angle = 0
route = []
start_time = time.time()

color_list =[]



reference_rgb = {"red_pink": (46, 17, 27), "olive_green": (15, 15, 9), "purple": (12, 10, 35), "blue": (10, 20, 33), "lime_green": (8, 27, 14)}


#color_calibration = [0, 0, 0]

# def median(val_lists):
#     """only use with lists of uneven lengths"""
#     calc_list = [[], [], []]
#     for val_list in (val_lists):
#         for i, val in enumerate(val_list):
#             calc_list[i].append(val)

#     out_list = []
#     for val_list in calc_list:
#         out_list.append(sorted(val_list)[int(len(val_list) / 2)])
#     return out_list

# def calibrate(rgb):
#     global color_calibration
#     rgb = list(rgb)
#     for i in range(len(rgb)):
#             rgb[i] = max(rgb[i], 1)
#     color_calibration = [reference_rgb["pink_red"][0] / rgb[0], reference_rgb["pink_red"][1] / rgb[1], reference_rgb["pink_red"][2] / rgb[2]]
#     #color_calibration = [0,0,0]
#     print("color_calibration:", color_calibration)

def ninety_degree_turn():
    print("Executing 90 degree turn")
    robot.straight(-60)
    robot.drive(80, -115)
    wait(2200)
    robot.straight(80)
    #robot.drive(0, 0)


def identify_color(rgb, return_with_number=False):
    #PLAN if we have issues with this function:
    # add another copy of the problematic color, with different color values.
    # put it in the dict as "black.2": (4, 4, 4)
    # return "black.2".split('.')[0]

    rgb = list(copy(rgb)) # don't modify original list

    similarity_dict = dict()

    for color_name, ref_values in reference_rgb.items():
        ref_similarity = []

        for i in range(3):
            rgb[i] = max(rgb[i], 1) # avoids division by zero after this for-loop

            ref_similarity.append((rgb[i] + 3) / (ref_values[i] + 3)) # the +3 are there to minimize issues with low brightness values.

        # explanation for the line below: if the red channel is p% lower than the reference, we want *all* channels to be p% lower than the reference.
        # If this is the case, the color may be the same as the reference color.
        #print(color_name, rgb)
        #print([abs(x-y) for x in ref_similarity for y in ref_similarity])
        difference = sum([abs(x-y) for x in ref_similarity for y in ref_similarity])
        # We also want to compare overall brightness:
        #print(avg(ref_similarity))
        difference += 2 * max(avg(rgb) / avg(ref_values), avg(ref_values) / avg(rgb)) - 1
        #print(max(avg(ref_similarity), 1 / avg(ref_similarity)) - 1)
        similarity_dict[color_name] = difference

    #not super useful prints
    # print(str(rgb))
    # print(similarity_dict)
    # print("min: ",  min(similarity_dict, key=similarity_dict.get))

    #useful print
    closest = sorted(similarity_dict, key=similarity_dict.get)
    print(str(round(time.time() - start_time, 3)) + "s:", str(rgb), " - closest colors:", closest[0], ": ", round(similarity_dict[closest[0]], 2), ", ", closest[1], ": ", round(similarity_dict[closest[1]], 2), ", ", closest[2], ": ", round(similarity_dict[closest[2]], 2))
    if return_with_number:
        return min(similarity_dict, key=similarity_dict.get)
    else:
        return min(similarity_dict, key=similarity_dict.get).split(".")[0]


# def robot_status(status):
#     print("The robot is " + str(status) + "right now")

# def feedback(color,beep_duration, beep_frequency):

#     # speaker.beep(beep_frequency, beep_duration)
#     # light.on(color)
#     return

def avg(list_of_stuff):
    return sum(list_of_stuff) / len(list_of_stuff)


def collision_avoidance():

    vehicle_detected = False
    ultra_distance = ultra_sensor.distance()
    if ultra_distance < 200:
        vehicle_detected = True  #initialize avoid sequence
        print("avoiding collision at " + str(round(time.time() - start_time, 3)) + "s. Distance: " + str(ultra_distance))

    if vehicle_detected:
        robot.straight(0)
        wait(2000)
        robot.drive(80, -120)
        wait(1400)
        robot.straight(700)
        wait(3000)
        robot.straight(0)
        wait(6000)
        robot.straight(-700)
        wait(3000)
        robot.drive(30, 120)
        wait(150)
        return True
    else:
        return False


def follow_line(times_passed,passed_line, turn_angle, instructions):
    print(' ')
    print(instructions)
    print(instructions[1])

    if collision_avoidance() == True:
        times_passed = 0

    if turn_angle > 130:
        times_passed +=1
        passed_line = False
        turn_angle = 30
        if int(times_passed) % 2 == 0:
            robot.drive(-40,turn_angle)
            wait(3000)
        else:
            robot.drive(-40,-turn_angle)
            wait(3000)

    if identify_color(left_light.rgb()) == "black":
        global goal_achieved
        goal_achieved = True
        robot.straight(0)
        wait(10000)
        robot.drive(80, -115)
        wait(4000)
        robot.straight(0)
        wait(3000)
    elif identify_color(left_light.rgb()) == instructions[1] and len(instructions) > 1: # Checks for next path-color
        print(instructions)
        instructions.pop(1)
        print(instructions)
        ninety_degree_turn()
        times_passed = 1
        print("Does 90 degrees turn")
    #elif left_light.color() != Color.WHITE and identify_color(left_light.rgb()) not in instructions:
     #   times_passed = 0
      #  robot.straight(-200)
       # wait(50)
    else:
        if int(times_passed) % 2 == 0:
            print("turning left")
            robot.drive(-30,turn_angle)
            # direction_toggle = robot.drive(-50,20)
        else:
            robot.drive(-30,-turn_angle)
            print("turning right")
            # direction_toggle = robot.drive(-50,-20)
        #--------------------------------------------------
        if passed_line == True and left_light.color() == Color.WHITE: # Passed line and on white
            passed_line = False
            turn_angle += 8
            times_passed += 1
            print("Passed line and on white")
        elif passed_line == False and left_light.color() != Color.WHITE: # On line
            print("On Line")
            turn_angle = 30
            passed_line = True
        elif passed_line == False and left_light.color() == Color.WHITE: # On white, haven't passed
            print("On white, haven't passed")
            turn_angle +=8
        print('Times: ',times_passed)
    return times_passed,passed_line, turn_angle




def main():
    turn_angle = 30
    goal_achieved = False
    global reference_rgb
    passed_line = False
    lines_passed = 0
    instructions = [identify_color(left_light.rgb()), "olive_green", "purple", "black"]
    reverse_instructions = instructions[::-1]
    reverse_instructions.pop(0)
    loop_continue = 0
    print("Robot will follow that following colors:", instructions)

    while loop_continue == 0:
        if goal_achieved == True:
            lines_passed, passed_line, turn_angle = follow_line(lines_passed, passed_line, turn_angle, reverse_instructions)
        print("Color: ", left_light.color())
        lines_passed, passed_line, turn_angle = follow_line(lines_passed, passed_line, turn_angle, instructions)

if __name__ == '__main__':
    sys.exit(main())
