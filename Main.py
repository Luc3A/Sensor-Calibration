import pyautogui
import time
import sys
import serial

import ImageData as image
import Sensor

# NOTE: openCV must be installed, but does not need to be imported
    # Install using <pip install opencv-python> 

### MAIN ###

ser = serial.Serial('COM6', 230400)

sensorIDS = Sensor.getSensorIDS()

# wait for sensor portal to load and if loading takes too long, alert user to possible issue
timeElapsed = 0

image.click(image.YostIcon)
while image.locate(image.DongleConnect) == 0:
    time.sleep(0.1)
    timeElapsed = timeElapsed + 0.5

    if timeElapsed > 60: 
        pyautogui.alert(text = "Yost Sensor Portal failed to load", title = 'Error', button = 'OK')
        sys.exit() # end program if too much time has passed


# Connect dongle and give time for connections
image.click(image.DongleConnect)

while(image.locate(image.NoSensorConnected)) == 0:
    time.sleep(0.1)

# locations used later 
sensorDropmenuX, sensorDropmenuY = pyautogui.locateCenterOnScreen(image.NoSensorConnected, confidence = 0.7)
dongleConnectX, dongleConnectY = pyautogui.locateCenterOnScreen(image.DongleConnect, confidence = 0.7)

x = 0
repeating = 0
left = 0
top = 0
for i in sensorIDS:
    x = x + 1
    # Connect sensor
    repeating, left, top = Sensor.connect(i, sensorDropmenuX, sensorDropmenuY, repeating, left, top)
    numCalibrationAttempts = 0

    # If sensor fails to calibrate too many times, alert user to possible issue
    while Sensor.calibrate(ser) == 0:
        numCalibrationAttempts = numCalibrationAttempts + 1

        if numCalibrationAttempts > 1: # if calibration fails too many times alert user and prompt response to end program to keep trying
            failureConfirm = pyautogui.confirm(text = "Calibration for sensor " + i + " failed " + numCalibrationAttempts + " times", title = 'Error', buttons = ['Try Again', 'Cancel'])
            if failureConfirm == 'Cancel':
                pyautogui.click(dongleConnectX, dongleConnectY)
                ser.close()
                sys.exit()


    numCommitAttempts = 0
    commited = 0
    while commited == 0: 
        numCommitAttempts = numCommitAttempts + 1
        # Commit settings 
        pyautogui.moveTo(dongleConnectX + 400, dongleConnectY)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('enter')
        

        # Give time to commit settings before disconnecting dongle 
        failure = 0
        while pyautogui.locateCenterOnScreen(image.CommandMenu, confidence = 0.9) == None and failure == 0:
            time.sleep(2)
            
            if image.locate(image.CommitFail) == 1:
                failure = 1
            

        if failure == 1: # exit out of notifications 
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.press('enter')

            if numCommitAttempts > 2: # if committing the settings fails too many times alert user 
                # the user can opt to cancel the calibration process or continue to attempt to commit settings
                failureConfirm = pyautogui.confirm(text = "Committing settings failed " + str(numCommitAttempts) + " times", title = 'Error', buttons = ['Try Again', 'Cancel'])
                if failureConfirm == 'Cancel':
                    time.sleep(1)
                    pyautogui.click(dongleConnectX, dongleConnectY)
                    ser.close()
                    sys.exit()
                if failureConfirm == "Try Again":
                    time.sleep(2)
        else:
            commited = 1

    # if there are still sensors that need to be calibrated prompt the user to place the next sensor into the holder         
    if x < len(sensorIDS):
        continueConfirm = pyautogui.confirm(text = "Please insert next sensor", title = "continue", buttons = ['OK', 'Cancel'])
        time.sleep(1)
        if continueConfirm == 'Cancel':
            pyautogui.click(dongleConnectX, dongleConnectY)
            ser.close()
            sys.exit() 

pyautogui.click(dongleConnectX, dongleConnectY)

ser.close()

pyautogui.alert(text = "Calibration process completed", title = '', button = "OK")

### End of code ###
