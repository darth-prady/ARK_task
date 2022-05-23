#!/usr/bin/env python
import rospy
import std_msgs
from std_msgs.msg import Int32
import numpy as np
import random
import os

pub1 = rospy.Publisher('/check2', Int32, queue_size=10)

def getDigits(num):
    return [int(i) for i in str(num)]

def noDuplicates(num):
    num_li = getDigits(num)
    if len(num_li) == len(set(num_li)):
        return True
    else:
        return False
  
def generateNum():
    while True:
        num = random.randint(1000,9999)
        if noDuplicates(num):
            return num
  
def guessCallback(data):
    global guess
    guess = data.data
    if not noDuplicates(guess):
        guess = None
        msg = Int32()
        msg.data = -999
        pub1.publish(msg)
        print("Please enter number without duplicates. Try again.")


def centsdollars():
    msg = Int32()
    c,b=0,0
    global guess,answer
    if guess < 1000 or guess > 9999:
        msg.data = -999
        pub1.publish(msg)
        print("Enter 4 digit number only. Try again.")
        return
    answer_li = getDigits(answer)
    guess_li = getDigits(guess)
    if guess == answer:
        print("You win!")
        print("The correct number is: " + str(answer))
        msg.data = 999
        pub1.publish(msg)
        os.system("rosnode kill /check2")
    else:
        for i,j in zip(answer_li,guess_li):        
        # common digit present
            if j in answer_li:
                # common digit exact match
                if j == i:
                    b += 2 
                # common digit match but in wrong position
                else:
                    c += 1
        msg.data = b+ c
        print("You have " + str(b) + " dollars and " + str(c) + " cents.")
        pub1.publish(msg)
        


def check1():
    global guess,answer
    guess = None
    answer = None
    rospy.init_node('check2')
    rospy.Subscriber("/guess_part2", Int32, guessCallback)
    answer = generateNum()
    print("Actual answer is ",answer)
    rate =rospy.Rate(10)
    while not rospy.is_shutdown():
        if guess is not None:
            centsdollars()
            guess = None

        rate.sleep()



if __name__ == '__main__':
    try:
        check1()
    except rospy.ROSInterruptException:
        pass