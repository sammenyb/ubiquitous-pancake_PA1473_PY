#!/usr/bin/env pybricks-micropython
import sys


# from project import __init__
# from project import pick_up as pu

from copy import copy

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

def avg(list_of_stuff):
    return sum(list_of_stuff) / len(list_of_stuff)

reference_rgb = {"black": (4, 5, 2),  # zeroes are NOT allowed in the values of this list.
"brown": (10, 6, 4),
"purple": (10, 9, 18), 
"yellow": (42, 36, 4), 
"pink_red": (37, 16, 13), 
"olive_green": (12, 13, 4), 
"lime_green": (8, 30, 8), 
"blue": (8, 19, 20), 
"white": (42, 47, 48),
"orange": (72, 23, 19), #not part of final track
"red": (49, 10, 13), #not part of final track
"red.2": (55, 14, 15) #not part of final track
}

def identify_color(rgb): #v3
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
    print(str(rgb), " - closest colors: ", closest[0], ": ", round(similarity_dict[closest[0]], 2), ", ", closest[1], ": ", round(similarity_dict[closest[1]], 2), ", ", closest[2], ": ", round(similarity_dict[closest[2]], 2))
    return min(similarity_dict, key=similarity_dict.get).split(".")[0]


fortsatt = 0
identify_color([51, 13, 13])
identify_color([54, 21, 22])
while fortsatt == 0:
    wait(400)
    farg = left_light.rgb()
    print("color rgb: " + str(farg) + ", current color: " + str(identify_color(farg)) + ", built-in detection of color: " + str(left_light.color()))

