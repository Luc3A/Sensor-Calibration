# Automatic Sensor Calibration 
## Motivation
Calibrating sensors by hand is tedious and annoying, so why not use a robot and save some time and effort


## What do I need? 
A laptop with the Yost sensor portal installed and two USB ports 


## Instructions 
### Before running the progeam: 
- The robot should be plugged into a USB port of the laptop that will be running the program.  The Yost sensor dongle should be connected to another USB port.
- The sensor should be turned on and make sure you know what logical ID the sensor is saved under on the dongle (ie. sensor 1 could be saved under logical ID 8 on the dongle)
- The sensor portal should be disconnected from the dongle before starting 

### Starting the code
- Run the program by navigating to the folder in the command line.
- Enter the line "python main.py".
- When prompted, enter the sensor logical ID (the code accepts an ID 0-14)

The program should handle the rest of the calibration process and will notify users when the calibration process had completed successfully or if the calibration failed too many times and something might be wrong.  

During the calibration process DO NOT move the mouse or move anything on the computer screen.  This will potentially mess up the process.  

Multiple sensors can be calibrated at a time.  The program will notify users when it is time to switch out the sensors in the holder.  
To calibrate multiple sensors without having to restart the code enter all the sensor IDs in the format (1 2 3 4 5) 

## How does it work? 
The program on the computer uses Pyautogui to interact with the Yost sensor portal and send commands to the robot using UART.  The robot moves position depending on the command and sends a command back through UART to signal to the program it can continue.  The robot uses an Adafruit CP2104 chip to provide power to a Raspberry Pi PICO and send UART signals.  The PICO outputs PWM signals to three servo motors in the robot depending on the command.  The servo motors are powered separately by a battery box with 4 AA batteries supplying ~6V to the servo motors.

Side note: if the servo motors are powered directly by the CP2104/computer that it is connected to, there is a high chance of shorting a circuit by drawing too much current from the computer.  If you are lucky this will just cause the computer to shut down and restart.  If you are unlucky (like me) you will fry a motherboard and need to get it replaced.  So don't try that if you decide to tweak this project.   


## What if I am unhappy with how the program works? 
;-;

### The program doesn't try recalibration enough times after the calibration fails 
If you want the program to try more calibration attempts before giving up, edit the main.py file where the code is instructed to retry calibration in the event of failure.  

### It runs too slowly
If you want to speed up the program, you can edit the wait times in the program files to be shorter (or longer).  I would be careful doing this as shortening the wait times too much can cause the program to run out of sync with the robot.  

## Somethings wrong what do I do? 
Panic ... but only for a minute.  Anymore than that is too much.    

### The robot isn't moving
If the program is running perfectly fine with the yost sensor portal but the robot isn't moving: it's probably out of battery.  The servos are powered with 4 AA batteries.  Open the base of the robot and replace the batteries.  Check to make sure the servo header pins did not come loose.

If the robot suddenly stopped moving in the middle of calibration it might have gotten some commands confused and froze.  Unplug everything for a minute and try again.  If the problem continues add more pauses to the code in between commands.  This will allow more time to process commands and help prevent confusion.  Open the PICO code and add some "time.sleep()" functions in between movements.  

If this doesn't work, you can control the robot directly using a terminal emulator to send commands directly.  (It accepts commands 0-23 and 100-103 as moveable positions but any entry should prompt a response from the PICO regardless).  Send these directly using a terminal emulator and it should move and print the commands back to you.  If it sends the commands back but nothing moves, the issue is with the servo power or the servos themselves.
If the command is not printed back it is an issue with the UART.  Check the CP2104 chip while sending commands.  When a command is sent a red light should blink and when a command is recieved it should blink green.  If the red light does not blink it is an issue with the serial connection and sending commands.  If the red light blinks but there is no green light there is an issue with the PICO.  Check the wiring and make sure there are no broken or dislocated wires.  

### The robot isn't moving to the correct positions
If the robot isn't moving to the correct position, it is most likely an issue with the PWM pulses sent from the PICO to the servo motors.  The PICO code can be accessed by plugging the PICO into a computer using a USB.  Once the code is accessed change the duty cycle variables that are sent to the servos. 

To easily test the position of the motors change the S#DEG# variables to the test position and call the following command after the helper functions are called but before the "while True:" loop: 
"moveServos(S1DEG#, S2DEG#, S3DEG#)" 
Then save the program and upload it to the PICO and the servos should move.  

If the duty cycle is too small or too high the servos may not move or will move continuously in a single direction.  A duty cycle between ~2000 - 8000 seems to work ok but above or below that may not.

### Serial port not found error
The serial port for the CP2104 is hardcoded into the main.py file.  If you are getting an error that the serial port is not found it could be registered by the computer with a different name.  Check the ports under device manager to see the new port name.  
It is also possible the computer is having an issue recognizing the device.  Download the CP210x USB to UART driver update from Silicon Labs and update the driver.  

### The program is interfacing with the Yost sensor portal strangely
The program uses pyautogui to find images on the screen and interact with buttons.  Pyautogui can be a little tricky sometimes.  Between beginning the project and ending the project it lost the ability to recognize a number of buttons on the sensor portal.  They all look pretty similar (same color, same text font, same size and shape) which can be confusing.  Depending on what part of the process is acting strange it could be that pyautogui began struggling to recognize an image.  In this case, the code should be changed to move the mouse to the exact coordinate of what should be clicked and click the mouse directly instead of trying to recognize an image of a button and select it.  This might take a bit of trial and error to determine the right coordinate to move to.  

### The calibration process keeps failing or the settings are failing to commit 
Yost is weird.  Try calibrating the sensors by hand and go through the process manually to see if there is something wrong with the settings in the process.  If something needs to be changed then edit the code to add this to the calibration process.  

### Part of the casing broke 
If any part of the casing broke/was damaged, the CAD files and full assembly are available.  Reprint the part and put everything back together.  

To reassemble connect the robot to a terminal emulator.  If you enter the command "100", the robot will move all the servos to 0 degrees.  From here, make sure everything is lined up and fasten everything into place.


## Suggestions for further development

### Structural issues
The robot tends to wobble quite a bit.  Some of this has been fixed by adding foam padding around joints.  Designing and external casing for the joints to hold them straight while still allowing for rotation would make movement smoother.  

### Working on the use of Pyautogui
Pyautogui struggles to recognize some images and instead of using these for points of reference, the code relies on moving to specific coordinates on the screen.  This may cause issues when moving the program to another computer.  I would reccomend figuring out how to use pyautogui better or finding a different way to control the yost portal.

### Supporting multiple sensors
Redesigning the robot to hold more sensors at a time would allow for a more efficient and hands off calibration process.  