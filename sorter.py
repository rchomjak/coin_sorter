import nxt

from nxt.sensor import *
from nxt.motor import *
import time

class Sorter (object):

    def __init__(self, motor_belt, motor_horizontal):

        self.belt = motor_belt
        self.horizontal = motor_horizontal 

        self.current_horizontal_position = None
        self.previous_horizontal_position = None

        self.coins_box_posistion = {1:'1', 2: '2', 3 : '3', 4:'0.5', 5:'0.20', 6:'0.10' }

        def set_horizontal_on_position(power=-20, turn=499, isbreak=False):
            self.horizontal.turn(power, turn, isbreak)
            self.current_horizontal_position = 5         

        set_horizontal_on_position()
        self.current_horizontal_position =5
        self.state_4(3)
        self.state_4(5)
        self.state_4(0)
        self.state_4(2)

    def state_1(self, power=-65, turn=200, isbreak=False):
       """Get a coin"""
       self.belt.turn(power, turn, isbreak);
       
    def state_2(self):
       """ Scan a coin """
       pass 

    def state_3(self):
        """ decide """
        pass


    def state_4(self, new_position):
        """ Move belt to position  """ 
        # |5|2|1|0.50|0.20|0.10|

        self.power_sign =-1
        self.to_position = 0

        def move_position(power=20, power_sign=-1, to_position=1, turn=84, isbreak=False):
            self.horizontal.turn(int(power*power_sign), abs(int(turn*to_position)), isbreak)
            

        self.to_position = new_position - self.current_horizontal_position   
        print(self.to_position)
        print(new_position)
        print(self.current_horizontal_position)

        if self.to_position == 0:
            return

        if self.to_position < 0 :
            self.power_sign = 1
       
        if new_position in [0, 5]:
            move_position(power_sign=self.power_sign, to_position=1, turn=499) 
        else:
            move_position(power_sign=self.power_sign, to_position=self.to_position)

        self.previous_horizontal_position = self.current_horizontal_position
        self.current_horizontal_position += self.to_position 


brick = nxt.find_one_brick();

print(brick)
motor_1 = Motor(brick, PORT_A)

print(motor_1)
motor_2 = Motor(brick, PORT_B)

#motor_2.turn(65, 100, brake=False)



sorter = Sorter(motor_1, motor_2)

#sorter.state_1()


#sorter.belt.turn_left


#main loop
'''
while True:

    # get coin - move belt until coin ni picture

    # scan coin

    # move to right container
    # |0.10|0.20|0.50|1|2|5|


    # drop coin

    pass
'''
