import cv2
import os, time
import HandTrackingModule as htm

path = "FingerImages"                               # Folder path name str
myLst = os.listdir(path)                            # Returns array of images listed inside dir

overlayImgs = []
for ImgPath in myLst:
    fingerImg = cv2.imread(f"{path}/{ImgPath}")     # Read single finger (.jpg) image inside dir
    overlayImgs.append(fingerImg)                   # Store read finger image


pastTime = 0    # Var to store previous time 
tipsIDs = [8, 12, 16, 20]   # Array to store each finger tip ID
outputMatrix = []           # Array to store output
count = 0                   # Counter to count number of fingers

detector = htm.handDetector(detectionCon=0.75)      # Creates a basic Hand detector

# Creates a basic webcam
video = cv2.VideoCapture(0)
while True:
    ret, img = video.read()

    # FINGER COUNTER MAIN PROCESS #
    img = detector.findHands(img)                           # Detects the Hands
    Landmarks = detector.findPosition(img, draw=False)      # Trace landmarks or position

    # If Landmarks list isn't empty
    if len(Landmarks) != 0:
        for i in range(len(tipsIDs)):

            # -> Say 100 is 6 and 0 is 8 -> So if 0 is below 100 then 'Finger is closed' -> ELSE -> if 0 is above 100 'Finger is opened'
            # IF PARTICULAR FINGER IS OPENED
            if Landmarks[tipsIDs[i]][2] < Landmarks[tipsIDs[i] - 2][2]:
                outputMatrix.append(1)

            # IF PARTICULAR FINGER IS CLOSED    
            if Landmarks[tipsIDs[i]][2] > Landmarks[tipsIDs[i] - 2][2]:
               outputMatrix.append(0)

        # print(outputMatrix)
        count = outputMatrix.count(1)
        print(count)
        outputMatrix = []       # Reset Matrix to zero


        # # INDEX FINGER #
        # if Landmarks[8][2] < Landmarks[6][2]:
        #     print("Index Finger is opened")
        # if Landmarks[8][2] > Landmarks[6][2]:
        #     print("Index Finder is closed")

        # # MIDDLE FINGER #
        # if Landmarks[12][2] < Landmarks[10][2]:
        #     print("Middle Finger is opened")
        # if Landmarks[12][2] > Landmarks[10][2]:
        #     print("Middle Finger is closed")
 
        # # RINGER FINGER #
        # if Landmarks[16][2] < Landmarks[14][2]:
        #     print("Ring Finger is opened")
        # if Landmarks[16][2] > Landmarks[14][2]:
        #     print("Ring Finger is closed")

        # # PINKY FINGER #
        # if Landmarks[20][2] < Landmarks[18][2]:
        #     print("Pinky Finger is opened")
        # if Landmarks[20][2] > Landmarks[18][2]:
        #     print("Pinky Finger is closed")

        # THUMB #
        # if Landmarks[4][2] < Landmarks[2][2]:
        #     print("Thumb is opened")
        # if Landmarks[4][2] > Landmarks[2][2]:
        #     print("Thumb is closed")


    # Declares height and width of the area to be used for overlaying finger img
    img[0:200, 0:200] = overlayImgs[count - 1]

    # Display FPS counter
    currentTime = time.time()                       # Store current time
    fps = 1/(currentTime - pastTime)                # Calculate FPS
    pastTime = currentTime                          # Put current time as past time
    # Defines -> TEXT, POSITION/ORIGIN, FONT, SCALE, COLOR, THICKNESS 
    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)       # Show time on main window

    cv2.imshow("Camera", img)
    
    key_pressed = cv2.waitKey(1)
    if key_pressed == ord('q'):
        break

video.release()
cv2.destroyAllWindows()