import cv2
import numpy as np
import nxt
from nxt.sensor import *
from nxt.motor import *
import time
import collections 


class Sorter (object):

    def __init__(self, motor_belt, motor_horizontal, motor_coin, video_url):

        self.belt = motor_belt
        self.horizontal = motor_horizontal
        self.motor_coin = motor_coin

        self.current_horizontal_position = None
        self.previous_horizontal_position = None

        self.coins_box_posistion = {'5': 5, '2': 4, '1': 3, '0.5': 2, '0.2': 1, '0.1': 0, 'ERROR': '-1'}
        self.coins_size = {71: '0.1', 80: '0.2', 90: '0.5', 110: '1', 95: '2', 115: '5', -1: 'ERROR'}

        cv2.namedWindow("preview")
        self.vc = cv2.VideoCapture(video_url)
        self.dequeue = collections.deque(maxlen=30)

        self.frame_counter = 50

        if self.vc.isOpened(): # try to get the first frame
            rval, frame = self.vc.read()
        else:
            raise(OSError, "Something is fucked")

        def set_horizontal_on_position(power=-20, turn=499, isbreak=False):
            self.horizontal.turn(power, turn, isbreak)
            self.current_horizontal_position = 5
        
        set_horizontal_on_position()

    def run_automata(self):
        self.computed_posistion = 0
        while True:
            self.state_1()
            self.state_2()
            self.computed_posistion = self.state_3()
            self.state_4(self.computed_posistion)
            self.state_5()

    def state_1(self, power=-65, turn=200, isbreak=False):
        # Get a coin
        self.push_coin()
        self.move_coin_to_camera()



    def push_coin(self):
            self.motor_coin.turn(25, 360, brake=True)

    def move_coin_to_camera(self, power=30, turn=80, isbreak=False):
        self.belt.turn(power, turn, isbreak)

    def state_2(self):
       """ Scan a coin """
       self.counter = 0
       self.dequeue.clear()
       while True  and self.counter < self.frame_counter:
            self.counter +=1
            rval, frame = self.vc.read()
            cv2.imshow("preview", frame)

            cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gauss_blur = cv2.GaussianBlur(cimg, (1, 1), -1)

            cv2.imshow('grayscale', gauss_blur)
            # _, binary_frame = cv2.threshold(gauss_blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            circles = cv2.HoughCircles(gauss_blur, cv2.HOUGH_GRADIENT, 1.2, 130,
                                                param1=100, param2=35, minRadius=68, maxRadius=110)
            # cv2.imshow('binary', binary_frame)
            #print(circles)
            if circles is not None:
             
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:

                    print("I guess it's a " + str(self.coins_size[min(self.coins_size, key=lambda x: abs(x-i[2]))]))
                    self.dequeue.append(i[2])
                    # draw the outer circle
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # draw the chttps://www.reddit.com/r/Iota/enter of the circle
                    #cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
            
                cv2.imshow('circle', frame) 
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                print(self.dequeue)
                break
       
       #cv2.destroyWindow("preview")
       #self.vc.release()
       #self.state_3();

    def state_3(self):
        """ decide """

        if self.dequeue.count == 0:
            #not found
            print("Empty queue")

        coin_radius_median = np.median(self.dequeue)
        print("coin radius " +  str(coin_radius_median))
        #-1 means ERROR
        coin_type = self.coins_size[min(self.coins_size, key=lambda x: abs(x - coin_radius_median))]
        print("coin_type " + str(coin_type))
        position = self.coins_box_posistion.get(coin_type, -1) 
        
        return position
        

    def state_4(self, new_position):
        """ Move belt to position  """
        # |5|2|1|0.50|0.20|0.10|

        self.power_sign =-1
        self.to_position = 0

        def move_position(power=20, power_sign=-1, to_position=1, turn=84, isbreak=False):
            self.horizontal.turn(int(power*power_sign), abs(int(turn*to_position)), isbreak)

        self.to_position = new_position - self.current_horizontal_position
        print("to position " + str(self.to_position))
        print("new_position " + str(new_position))
        print("current position" + str(self.current_horizontal_position))

        if self.to_position == 0:
            return

        if self.to_position < 0:
            self.power_sign = 1

        if new_position in [0, 5]:
            move_position(power_sign=self.power_sign, to_position=1, turn=499)
        else:
            move_position(power_sign=self.power_sign, to_position=self.to_position)

        self.previous_horizontal_position = self.current_horizontal_position
        self.current_horizontal_position += self.to_position

    def state_5(self, power=65, turn=200, isbreak=False):
        """Get of coin"""
        self.belt.turn(power, turn, isbreak)


brick = nxt.find_one_brick()

print(brick)
motor_1 = Motor(brick, PORT_A)

print(motor_1)
motor_2 = Motor(brick, PORT_B)


motor_3 = Motor(brick, PORT_C)
print(motor_3)

# print("acout to turn it")
# motor_3.turn(25, 360, brake=True)

# motor_1 = None
# motor_2 = None

sorter = Sorter(motor_1, motor_2, motor_3, 'http://192.168.52:4747/mjpegfeed?640x480')
sorter.run_automata()


'''
while True:

    # get coin - move belt until coin ni picture

    # scan coin

    # move to right container
    # |0.10|0.20|0.50|1|2|5|


    # drop coin

    pass
'''
