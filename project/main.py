#!/usr/bin/env pybricks-micropython
from copy import copy
import sys

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
route = []
start_time = time.time()

reference_rgb = {"red_pink": (46, 17, 27), "olive_green": (15, 15, 9), "purple": (12, 10, 35), "blue": (10, 20, 33), "lime_green": (8, 27, 14)}

def ninety_degree_turn():
    """Turns the robot ninety degrees to the right, and tries to reposition the robot so that the color sensor ends up approximately where it was before the turn."""
    print("Executing 90 degree turn")
    robot.straight(-60)
    robot.drive(80, -115)
    wait(2200)
    robot.straight(80)

def identify_color(rgb, return_with_number=False):
    """Attempts to identify the color in rgb, which should be a list or tuple with red, green, and blue color values expressed as numbers between 0 and 100.\n
    Returns the name of the identified color as a string."""
    # Potential solution if we have issues with this function:
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
        difference = sum([abs(x-y) for x in ref_similarity for y in ref_similarity])

        # We also want to compare overall brightness:
        difference += 2 * max(avg(rgb) / avg(ref_values), avg(ref_values) / avg(rgb)) - 1

        similarity_dict[color_name] = difference

    closest = sorted(similarity_dict, key=similarity_dict.get)
    print(str(round(time.time() - start_time, 3)) + "s:", str(rgb), " - closest colors:", closest[0], ": ", round(similarity_dict[closest[0]], 2), ", ", closest[1], ": ", round(similarity_dict[closest[1]], 2), ", ", closest[2], ": ", round(similarity_dict[closest[2]], 2))

    if return_with_number:
        return min(similarity_dict, key=similarity_dict.get)
    else:
        return min(similarity_dict, key=similarity_dict.get).split(".")[0]


def avg(list_of_stuff):
    """Returns the average value in a list."""
    return sum(list_of_stuff) / len(list_of_stuff)


def collision_avoidance():
    """Detects an imminent collision with ultra_sensor, and makes an evasive maneuver if needed.\n
    Returns a bool that indicates whether or not a collision avoidance attempt was made."""
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


def follow_line(times_passed: int,passed_line: bool, turn_angle: int, instructions: list[str]):
    """Initiates the following of the lines.\n
    Returns: times_passed: int, passed_line: bool, turn_angle: int"""
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
    else:
        if int(times_passed) % 2 == 0:
            print("turning left")
            robot.drive(-30,turn_angle)
        else:
            robot.drive(-30,-turn_angle)
            print("turning right")
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
    return times_passed, passed_line, turn_angle




def main():
    """Main function. Runs at start."""
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

