# Project 6: LED turns ON for 5 seconds on button press - the use of timers in Arduino

1. Understand the use of timers in Arduino and problems that they can solve

## Write a program that does the following:
- Turn on an LED on pin 4 when a button is pressed using interrupts
- The LED should turn off after 5 seconds
- Do not use a delay() function here. Please use the system clock to measure the time. look for the millis() function in the Arduino reference.
Test the code and make sure it works as expected
paste a screen shot from the logic analyzer below:

![internal clock screenshot](<internal clock screenshot-1.png>)
 
## update the code to add a delay in the loop function
- Add the same for loop as in the previous exercise to simulate a long process. Does the LED still turn off after 5 seconds? Why or why not?
answer here: It doesnt due to the background claculation. Since the claculation runs in the background millis doesn't have the opportunity to check the time
add a screen shot from the logic analyzer below:

![internal clock with time wasting loop](<internal clock with time wasting loop-1.png>)

## Write a second program. The proper way to solve this problem is to use a timer
- install package mstimer2 from the library manager
- read the readme file of the package and note the package limitations
- open an example of the package, examine the code and its functions and how to use them.
- implement a timer to turn off the LED after 5 seconds
- note the callback in the timer. When is it called?

## Exercises
- check that although there is delay in the loop function, the LED now turns off after 5 seconds

- change the LED time ON from 5 seconds to 30 ms, measure in the scope the time the LED is ON. is it 30 ms? Why or why not?
answer here: there is a around 50usec difference. this could be due to the timer code limitations, or hardware issue and an error of 1-2 sample in the cursor positioning.
paste a screen shot from the scope below:

![30msTimer](30msTimer-1.png)