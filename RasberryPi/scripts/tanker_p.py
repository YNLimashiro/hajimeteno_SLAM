#!/usr/bin/env python
import rospy
from tanker.msg import input_keys
import pygame
from pygame.locals import *
import sys

"""
node:controller
topic:command
message:input_keys
"""


def talker():
    rospy.init_node('controller', anonymous=False)
    publisher = rospy.Publisher('command', input_keys, queue_size=10)
    pygame.init()
    screen = pygame.display.set_mode((300,300))
    pygame.display.set_caption("key")
    keys = input_keys()
    while not rospy.is_shutdown():
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    keys.left = 1
                elif event.key == K_RIGHT:
                    keys.right = 1
                elif event.key == K_UP:
                    keys.up = 1
                elif event.key == K_DOWN:
                    keys.down = 1
                elif event.key == K_ESCAPE:
                    sys.exit()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    keys.left = 0
                elif event.key == K_RIGHT:
                    keys.right = 0
                elif event.key == K_UP:
                    keys.up = 0
                elif event.key == K_DOWN:
                    keys.down = 0


        rospy.loginfo(keys)
        publisher.publish(keys)
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
