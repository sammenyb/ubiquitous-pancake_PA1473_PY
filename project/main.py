#!/usr/bin/env pybricks-micropython
from copy import copy
# from msilib.schema import ControlCondition
import sys

# import statistics
# list_test = [3,2,1,5,5]
# print(statistics.median([3,2,5,5]))
# from project import __init__
# from project import pick_up as pu



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
    robot.straight(170)
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
    if ultra_distance < 320:
        vehicle_detected = True  #initialize avoid sequence
        print("avoiding collision at " + str(round(time.time() - start_time, 3)) + "s. Distance: " + str(ultra_distance))

    if vehicle_detected:
        robot.straight(0)
        wait(2000)
        return
        robot.turn(-70)
        robot.straight(-200)
        robot.turn(90)
        robot.straight(-300)

    return



def follow_line(colors):
    copy_colors_reverse = colors[::-1]
    print(copy_colors_reverse)
    #print(choosen_warehouse)
    global angle, speed, color_list
    continue_driving = 0 # does this need to be an int?
    while continue_driving == 0:
        collision_avoidance()
        color_left = left_light.rgb()
        if avg(color_left) == 0:
            color_left = (1,0,0) #avoid div by 0

        adj_color_left = [color_calibration[0] * color_left[0], color_calibration[1] * color_left[1], color_calibration[2] * color_left[2]]
        for i in range(len(adj_color_left)):
            adj_color_left[i] = max(adj_color_left[i], 1)

        color_list.append(adj_color_left)
        if len(color_list) > 5:
            color_list.pop(0)
        med_value = median(color_list)

        med_color = identify_color(med_value)
        current_color = identify_color(adj_color_left)


        robot_status(status="Searching for " + str(colors) + ", and following " + str(current_color) + " line")

        color_multiplier = 1 / avg(reference_rgb[identify_color(adj_color_left, True)])
        # this always looks at the first one in the list!

        if len(colors) >= 2 and current_color == colors[1]:
            speed *= 0.15
            angle *= 0.17
        robot.drive(-speed, -angle)

        if len(colors) == 1:
            colors = copy_colors_reverse
        elif current_color != "white" and current_color != colors[0] and current_color != colors[1]:
            angle = 0
            speed = 30
        elif len(colors) > 1 and med_color == colors[1]:
            colors.pop(0)
            print("changing color - found ", current_color)
            print(colors)
            if colors[0] != "black":
                ninety_degree_turn()
            else:
                print("detected black. Turning around.")
                robot.turn(170)
        elif current_color == "white":
            angle = -26# * avg(color_left) * color_multiplier
            speed = 55
        elif 2.2 < avg(color_left) * color_multiplier and current_color != colors[0]:
            angle = -12 * avg(color_left) * color_multiplier
            speed = 40
        elif 1.2 <= avg(color_left) * color_multiplier <= 2.2 and current_color != colors[0]:
            angle = 0
            speed = 45
        else:
            relative_brightness = (avg(color_left) * color_multiplier) ** 2
            if relative_brightness < 0.8:
                relative_brightness = 0.8
            if current_color == "red_pink":
                relative_brightness -= 0.2
            angle = 75 / relative_brightness #how much the robot turns when colored line is detected

            speed = min(50, 20 * relative_brightness - 58)


        ''''
        if not current_color == "white" and len(route) == 0:
            route.append(current_color)
            print("route: " + str(route))
        elif not current_color == "white" and (str(route[-1]) != str(current_color)):
            route.append(current_color)
            print("route: " + str(route))
            print("Test route:" + str(route[-1]) + " , " + str(current_color))
        print("speed " + str(speed) + ", angle " + str(angle))
        '''

def reports(instructions):
    print('instructions that will be performed: ', instructions)

def cranelift():
    pass
    #print("motor angle " + str(crane_motor.angle()))
    crane_motor.run_angle(15, -10, wait=True)
    # crane_motor.run_angle(15, 60, wait=True)

def main_tmp():

    #correction = (30-left_light.reflection())*2
    correction = left_light.reflection()
    print(correction)
    if 50 < ultra_sensor.distance() < 100:
            robot.drive(0,0)

    elif ultra_sensor.distance() < 50:
        robot.drive(20,0)
    else:
        if 40 <= correction <= 60: # Drives straight forward
            robot.drive(-100,0)

        elif 30 < correction < 40: # ini Begining to detect color
            robot.drive(-50,-5)

        elif 20 < correction <= 30: # Starting to detect color
            robot.drive(-25,-20)

        elif correction <= 20: # Dark, at color, turn right a lot
            passed_line = False
            lines_passed = 0
            while lines_passed != 10:
                lines_passed, passed_line = drive_tmp(lines_passed,passed_line)

            print('sharp')

        elif 61 < correction <= 70 : # Beginging to detect white
            robot.drive(-50, 5)

        elif  70 < correction < 80: #a lot of white, turn left
            robot.drive(-50, 20)

        elif 81 <= correction: #Only white is detected turn left
            robot.drive(-10, 50)

def drive_tmp(times_passed,passed_line):
    print(' ')
    if int(times_passed) % 2 == 0:
        print("turning left")
        robot.drive(-80,120)
        # direction_toggle = robot.drive(-50,20)
    else:
        robot.drive(-80,-120)
        print("turning right")
        # direction_toggle = robot.drive(-50,-20)
    #--------------------------------------------------
    if left_light.reflection() >= 70 and passed_line == True: # Passed line and on white
        passed_line = False
        times_passed += 1
        print("Passed line and on white")
    elif left_light.reflection() < 70 and passed_line == False: # On line
        print("On Line")
        passed_line = True
    elif left_light.reflection() > 80 and passed_line == False: # On white, haven't passed
        print("On white, haven't passed")
    print('Times: ',times_passed)
    return times_passed,passed_line





    # if passed_line == False and left_light.reflection() >= 70:
    #     direction_toggle

    # elif left_light.reflection() < 70:
    #     direction_toggle
    #     passed_line = True
    #     print("On Line")

    # elif passed_line == True and left_light.reflection() >= 70:
    #     += 1

    #     print("Changing direction")


def main():
    #turn_angle = 60
    passed_line = False
    lines_passed = 0
    instructions = [identify_color(left_light.rgb()), "olive_green", "blue"]
    loop_continue = 0
    calibrate(left_light.rgb())
    #cranelift()
    reports(instructions)
    while loop_continue == 0:
        print("Reflection: ", left_light.reflection())
        print("Color: ", left_light.color())
        """ihuiedhcid()"""
        # follow_line(instructions)
        # main_tmp()
        lines_passed, passed_line = drive_tmp(lines_passed,passed_line)


if __name__ == '__main__':
    sys.exit(main())
if __name__ == '__main__':
    sys.exit(main())