#!/usr/bin/env python

from __future__ import print_function

import rospy

from sensor_msgs.msg import Joy

import pygame
from pygame.locals import *

#import subprocess

import sys, select, termios, tty, fcntl, os


msg = """

"""

class JoyPub:
    def __init__(self):
        self.settings_ = termios.tcgetattr(sys.stdin)
        self.joy_pub = rospy.Publisher('/robot/joy', Joy, queue_size = 1)

        self.stop_ = rospy.get_param("~stop", 0.5)
        self.button_flg = [0]*11
        self.joy_axis = [0]*6
        self.hand_status = 0
        self.motion = 0
        self.start_flg = 1

        pygame.init()
        pygame.joystick.init()
        try:
            self.j = pygame.joystick.Joystick(0)# create a joystick instance
            self.j.init() # init
            print('Joystick: ' + self.j.get_name())
            print('bottun : ' + str(self.j.get_numbuttons()))
            pygame.event.get()
            
        except pygame.error:
            print('No connect joystick')
            print('exit')
            pygame.quit()
            sys.exit()

        finally:
            msg = Joy()
            msg.axes = [0]*8
            msg.buttons = [0]*11
            self.joy_pub.publish(msg)
            #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)
 
    # Intializes everything
    def main(self):
        try:
            while(1):
                msg = Joy()
                msg.axes = [0]*8
                msg.buttons = [0]*11
                
                for e in pygame.event.get(): #event check
                    if e.type == QUIT: # is pushed quit
                        pygame.quit()
                        return
                    if e.type == KEYDOWN:
                        if e.key  == K_ESCAPE: # is pushed escape
                            pygame.quit()
                            sys.exit()
                    # check event with controler
                    if e.type == pygame.locals.JOYAXISMOTION: # 7
                        for i in range(6):
                            self.joy_axis[i] = self.j.get_axis(i)
                            #if((self.joy_axis[i] < 10e-3) and (self.joy_axis[i] > -10e-3)):
                            #    self.joy_axis[i] = 0
                            if(self.joy_axis[i] > 0.5):
                                self.joy_axis[i] = -1
                            elif(self.joy_axis[i] < -0.5):
                                self.joy_axis[i] = 1 
                            else:
                                self.joy_axis[i] = 0  

                        print('Rx' + '{:.4}'.format(str(self.joy_axis[3])) + \
                              'Ry' + '{:.4}'.format(str(self.joy_axis[4])) + \
                              'Rz' + '{:.4}'.format(str(self.joy_axis[5])) + \
                              'Lx' + '{:.4}'.format(str(self.joy_axis[0])) + \
                              'Ly' + '{:.4}'.format(str(self.joy_axis[1])) + \
                              'Lz' + '{:.4}'.format(str(self.joy_axis[2])) )
                              
                        msg.axes[0] = -self.joy_axis[0]
                        msg.axes[1] = -self.joy_axis[1]

                        self.joy_pub.publish(msg)

                        msg.axes = [0]*8
                        msg.buttons = [0]*11
                        
                    elif e.type == pygame.locals.JOYBALLMOTION: # 8
                        print('ball motion')

                    elif e.type == pygame.locals.JOYHATMOTION: # 9
                        print('hat motion')

                    elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
                        for i in range(self.j.get_numbuttons()):# read button
                            if(e.button == i):
                                self.button_flg[i] = 1

                        print(  'A' + str(self.button_flg[0]) + \
                                'B' + str(self.button_flg[1]) + \
                                'X' + str(self.button_flg[2]) + \
                                'Y' + str(self.button_flg[3]) + \
                                'LB' + str(self.button_flg[4]) + \
                                'RB' + str(self.button_flg[5]) + \
                                'BACK' + str(self.button_flg[6]) + \
                                'START' + str(self.button_flg[7]) + \
                                'Logicool' + str(self.button_flg[8]) + \
                                'StL' + str(self.button_flg[9]) + \
                                'StR' + str(self.button_flg[10]))    

                    elif e.type == pygame.locals.JOYBUTTONUP: # 11
                        for i in range(self.j.get_numbuttons()):
                            if(e.button == i):
                                self.button_flg[i] = 0
                            
                        print(  'A' + str(self.button_flg[0]) + \
                                'B' + str(self.button_flg[1]) + \
                                'X' + str(self.button_flg[2]) + \
                                'Y' + str(self.button_flg[3]) + \
                                'LB' + str(self.button_flg[4]) + \
                                'RB' + str(self.button_flg[5]) + \
                                'BACK' + str(self.button_flg[6]) + \
                                'START' + str(self.button_flg[7]) + \
                                'Logicool' + str(self.button_flg[8]) + \
                                'StL' + str(self.button_flg[9]) + \
                                'StR' + str(self.button_flg[10]))    
        except Exception as e:
            print(e)
        finally:
            msg = Joy()
            msg.axes = [0]*8
            msg.buttons = [0]*11
            self.joy_pub.publish(msg)
            #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)



if __name__=="__main__":
    rospy.init_node('controller_joy')

    jp = JoyPub()

    jp.main()

