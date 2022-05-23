#!/usr/bin/env python
import rospy
import std_msgs
from std_msgs.msg import Int32
import numpy as np
import random
import os

pub1 = rospy.Publisher('/check2', Int32, queue_size=100)

tries = 0

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
    global guess,answer,tries
    msg = Int32()
    c,b=0,0
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
    else:
        tries+=1
        for i,j in zip(answer_li,guess_li):        
            if j in answer_li:
                if j == i:
                    b += 2 
                else:
                    c += 1
        msg.data = b+ c
        # print("You have " + str(b) + " dollars and " + str(c) + " cents.")
        pub1.publish(msg)
        


def check2():
    global guess,answer,tries
    guess = None
    answer = None
    rospy.init_node('check2')
    rospy.Subscriber("/guess_part2", Int32, guessCallback)
    answer = generateNum()
    print("Actual answer is ",answer)
    while not rospy.is_shutdown():
        if guess is not None:
            centsdollars()
            tries+=1
            guess = None



if __name__ == '__main__':
    try:
        check2()
    except rospy.ROSInterruptException:
        pass