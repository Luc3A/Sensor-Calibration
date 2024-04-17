import pyautogui
import time 
import sys 
import serial
import ImageData as image

# open calibration menu and go through calibration process
def calibrate(ser): 

    # navigate through sensor calibration menu to gradient descent
    image.click(image.SensorMenu)

    while image.locate(image.CalibrationIcon) == 0: 
        time.sleep(0.1)
        image.click(image.SensorMenu)

    IconX, IconY = pyautogui.locateCenterOnScreen(image.CalibrationIcon, confidence = 0.7)
    pyautogui.moveTo(IconX, IconY, 0.1)

    while image.click(image.GradientDescent) == 0:
        time.sleep(0.1) 


    # uncheck compass box (otherwise calibration will fail)    
    while image.locate(image.MarkedCheckBox) == 0:
        time.sleep(0.1)

    while image.locate(image.CompassBox) == 0:
        time.sleep(0.1)
        
    compassCenterX, compassCenterY = pyautogui.locateCenterOnScreen(image.CompassBox, confidence = 0.7)
    pyautogui.moveTo(compassCenterX - 82.5, compassCenterY) 

    pyautogui.click() 
    
    # begin calibration process
    pyautogui.move(-150,190,0.2)
    pyautogui.click() 

    pyautogui.move(200,675,0.5)

    for i in range(24):

        step = (str(i) + '\n') 
        ser.write(step.encode()) # send position to robot 

        line = ser.read_until(b'\r\n') # wait to recieve serial message back indicating robot has moved

        time.sleep(1)

        pyautogui.click()

        time.sleep(2) # pause to allow next screen to load
        
    # select "finish"
    time.sleep(1)
    pyautogui.move(220,0)
    pyautogui.click()

    time.sleep(0.5)
    pyautogui.press('enter')
    flag = 0
    while flag == 0:
        
    # At this point, calibration either fails or is successful.  Main code deals with failure case 
        if image.locate(image.CalibrationFailure) == 1:
            flag = 1
            pyautogui.press('enter')
            time.sleep(0.1)
            image.click(image.YostIcon)
            return 0

        if image.locate(image.CalibrationSuccessful) == 1:
            flag = 1
            pyautogui.press('enter')
            time.sleep(0.1)
            image.click(image.YostIcon)
            return 1

        time.sleep(0.1) 

# get a list of what sensors to calibrate
def getSensorIDS():
    flag = False # flag used to determine validity of entry

    while flag == False:
        flag = True
        sensorIDS = pyautogui.prompt(text = 'Enter IDs', title = 'Enter sensor ID (0 - 14)', default = '')
        
        # turn the string into a list 
        sensorIDS = list(sensorIDS.split(" "))

        for i in sensorIDS: 
            # only accept integer numbers as an entry
            if i.isdigit():
                # only accept an integer 0-14 (Valid sensor IDs)
                if int(i) > 14:
                    flag = False # if item in list is not an integer, entry is invalid 

            else:
                if i == '': 
                    sensorIDS.remove(i) # Remove the blank space from the end of the list  
                else:
                    flag = False
        
        if len(sensorIDS) == 0:
            flag = False # If entry is empty, it is invallid 

        #if len(sensorIDS) > 1:
            #flag = False # Currently can only calibrate one sensor at a time

        if flag == False: 
            # If entry is invalid, notify user and redo prompt 
            pyautogui.alert(text = "Invalid Entry Please Reenter", title = 'Error', button = 'OK') 
    
    # Return the list of IDs 
    return sensorIDS


def connect(sensorID, X, Y, repeating, left, top):
    # open sensor menu
    pyautogui.click(X, Y)

    time.sleep(0.2)
    # select sensor ID from menu
    if repeating == 0:
        menuLocation = pyautogui.locateOnScreen(image.SensorConnectOptions)
        left = menuLocation[0] + 50
        top = menuLocation[1] + 105

    pyautogui.click(left, top - 82.5 + (float(sensorID) * 42.5))

    repeating = 1

    return repeating, left, top
