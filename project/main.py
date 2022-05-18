#!/usr/bin/env pybricks-micropython
from copy import copy
# from msilib.schema import ControlCondition
import sys

# import statistics
# list_test = [3,2,1,5,5]
# print(statistics.median([3,2,5,5]))
# from project import __init__
# from project import pick_up as pu
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
"blue": (8, 19, 22),
#"blue.2": (9, 17, 30),
#"blue.2": (14, 28, 75),
"white": (93, 83, 95),
#"white.2": (40, 38, 36)
#"orange": (72, 23, 19), #not part of final track
#"red": (49, 10, 13), #not part of final track
#"red.2": (55, 14, 15) #not part of final track
}

color_calibration = [0, 0, 0]

def median(val_lists):
    """only use with lists of uneven lengths"""
    calc_list = [[], [], []]
    for val_list in (val_lists):
        for i, val in enumerate(val_list):
            calc_list[i].append(val)

    out_list = []
    for val_list in calc_list:
        out_list.append(sorted(val_list)[int(len(val_list) / 2)])
    return out_list

def calibrate(rgb):
    global color_calibration
    rgb = list(rgb)
    for i in range(len(rgb)):
            rgb[i] = max(rgb[i], 1)
    color_calibration = [reference_rgb["pink_red"][0] / rgb[0], reference_rgb["pink_red"][1] / rgb[1], reference_rgb["pink_red"][2] / rgb[2]]
    #color_calibration = [0,0,0]
    print("color_calibration:", color_calibration)
"""
test_text = ""
def msg(text):
    ev3.screen.clear()
    ev3.screen.draw_text(20, 50, text)
"""
def ninety_degree_turn():
    print("Executing 90 degree turn")
    robot.straight(-60)
    robot.drive(80, -115)
    wait(2000)
    robot.straight(100)
    #robot.drive(0, 0)


def identify_color(rgb, return_with_number=False): #v3
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


def robot_status(status):
    print("The robot is " + str(status) + "right now")

def feedback(color,beep_duration, beep_frequency):

    # speaker.beep(beep_frequency, beep_duration)
    # light.on(color)
    return

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
        wait(300)
        return True
    else:
        return False


def cal_color():
    print('')
    reference_rgb = {}
    reference_rgb["blue"] = left_light.rgb()
    print("TRUE RGB Blue: ",left_light.rgb())

    wait(5000)
    ev3.speaker.beep()
    reference_rgb["red_pink"] = left_light.rgb()
    print("TRUE RGB Red_Pink: ",left_light.rgb())

    wait(5000)
    ev3.speaker.beep()
    reference_rgb["purple"] = left_light.rgb()
    print("TRUE RGB Purple: ",left_light.rgb())

    wait(5000)
    ev3.speaker.beep()
    reference_rgb["red_pink"] = left_light.rgb()
    print("TRUE RGB 2: ",left_light.rgb())

    wait(5000)
    ev3.speaker.beep()
    reference_rgb["olive_green"] = left_light.rgb()
    print("TRUE RGB Olive_green: ",left_light.rgb())

    wait(5000)
    ev3.speaker.beep()
    reference_rgb["lime_green"] = left_light.rgb()
    print("TRUE RGB lime_green: ",left_light.rgb())

    print('Dict',reference_rgb)
    file = open("colors.csv", "w")
    writer = csv.writer(file)
    for key, value in reference_rgb.items():
        writer.writerow([key, value])

    file.close()
    
    return reference_rgb
       
    # "brown": (10, 6, 4),
    # "purple": (8, 9, 20),
    # "purple.2": (12, 7, 37),
    # "yellow": (42, 36, 4),
    # "pink_red": (36, 16, 13),
    # "pink_red.2": (30, 15, 20),
    # "olive_green": (12, 15, 4),
    # "olive_green.2": (10, 15, 9),
    # "lime_green": (8, 30, 8),
    # "blue": (8, 19, 22)

def reports(instructions):
    print('instructions that will be performed: ', instructions)

def cranelift():
    pass
    #print("motor angle " + str(crane_motor.angle()))
    crane_motor.run_angle(15, -10, wait=True)
    # crane_motor.run_angle(15, 60, wait=True)

def pick_up():

    #correction = (30-left_light.reflection())*2
    correction = left_light.reflection()
    print(correction)
    if correction == 0:
            robot.drive(0,0)

    elif ultra_sensor.distance() < 50:
        robot.drive(20,0)
    else:
        if 40 <= correction <= 60: # Drives straight forward
            robot.drive(-30,0)

        elif 30 < correction < 40: # ini Begining to detect color
            robot.drive(-30,-5)

        elif 20 < correction <= 30: # Starting to detect color
            robot.drive(-25,-20)

        elif correction <= 20: # Dark, at color, turn right a lot
            robot.drive(-25,-50)

            print('sharp')

        elif 61 < correction <= 70 : # Beginging to detect white
            robot.drive(-50, 5)

        elif  70 < correction < 80: #a lot of white, turn left
            robot.drive(-50, 20)

        elif 81 <= correction: #Only white is detected turn left
            robot.drive(-10, 50)


def drive_tmp(times_passed,passed_line, turn_angle, instructions):
    print(' ')
    print(instructions)
    print(instructions[1])
   
    if collision_avoidance() == True:
        times_passed = 0  
    if identify_color(left_light.rgb()) == "black":
        global goal_achieved
        goal_achieved = True
        robot.straight(0)
        wait(10000)
        robot.drive(80, -115)
        wait(4000)
        robot.straight(0)
        wait(3000)
    if turn_angle > 130:
        times_passed +=1
        passed_line = False
        turn_angle = 30 
        if int(times_passed) % 2 == 0:
            robot.drive(-30,turn_angle)
            wait(3000)
        else:
            robot.drive(-30,-turn_angle)
            wait(3000)
        print("fixed_itself fixed itself fixed\n itselffixed_itself fixed itself fixed itselffixed_itself fixed itself fixed itselffixed_itself fixed itself fixed itselffixed_itself fixed itself fixed itselffixed_itself fixed itself fixed itselffixed_itself fixed itself fixed itself")
    elif identify_color(left_light.rgb()) == instructions[1] and len(instructions) > 1: # Checks for next path-color
        print(instructions)
        instructions.pop(1)
        print(instructions)
        ninety_degree_turn()
        times_passed = 1
        print("Does 90 degrees turn")
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
    # reference_rgb = cal_color()
    passed_line = False
    lines_passed = 0
    instructions = [identify_color(left_light.rgb()), "olive_green", "blue", "black"]
    print(instructions)
    reverse_instructions = instructions[::-1]
    reverse_instructions.pop(0)
    loop_continue = 0
    # calibrate(left_light.rgb())
    #cranelift()
    reports(instructions)

    while loop_continue == 0:
        if goal_achieved == True:
            lines_passed, passed_line, turn_angle = drive_tmp(lines_passed, passed_line, turn_angle, reverse_instructions)
        print("Color: ", left_light.color())
        """ihuiedhcid()"""
        lines_passed, passed_line, turn_angle = drive_tmp(lines_passed, passed_line, turn_angle, instructions)

if __name__ == '__main__':
    sys.exit(main())
