import cv2
import numpy as np
from matplotlib import pyplot as plt
import keyboard

# Connecting to webcam
# cap = cv2.VideoCapture(0)
# # Read frames
# ret, frame = cap.read()
# print(frame)
# cv2.imwrite("testshot.jpg", frame)
# # Release the capture
# cap.release()

# Hough Circle Detection parameters
param1 = 28
param2 = 50
minRadius = 20
maxRadius = 135

def shot():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite("testshot.jpg", frame)
    cap.release()


def continuous_detection():

    # Print slider values
    def print_bar(x):
        print(x)

    # Open webcam and set video size
    cap = cv2.VideoCapture(3)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Parameter settings window
    img = np.zeros((300, 300, 3), np.uint8)
    cv2.namedWindow("preview")
    #   Sliders
    cv2.createTrackbar('param1', "preview", 28, 500, print_bar)
    cv2.createTrackbar('param2', "preview", 50, 500, print_bar)
    cv2.createTrackbar('minRadius', "preview", 20, 500, print_bar)
    cv2.createTrackbar('maxRadius', "preview", 135, 500, print_bar)

    while True:
        # Read webcam input
        output = cap.read()[1]
        # Process image
        grey = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.GaussianBlur(grey, (25, 25), cv2.BORDER_DEFAULT)
        blur2 = cv2.GaussianBlur(blur1, (25, 25), cv2.BORDER_DEFAULT)
        blur3 = cv2.bilateralFilter(blur2, 9, 75, 75)
        # Hough Circle detection
        circles = cv2.HoughCircles(blur3, cv2.HOUGH_GRADIENT, 1.2, 100, param1=cv2.getTrackbarPos("param1", 'preview'), param2=cv2.getTrackbarPos("param2", 'preview'), minRadius=cv2.getTrackbarPos("minRadius", 'preview'), maxRadius=cv2.getTrackbarPos("maxRadius", 'preview'))
        # Detection Graphics per circle
        if circles is not None:
            circles = np.round(circles[0, :]).astype('int')
            count = 1
            for i in circles:
                # draw the circle in the output image, then draw a rectangle in the image
                # corresponding to the center of the circle
                cv2.circle(blur2, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(blur2, (i[0], i[1]), 2, (0, 0, 255), 3)
                cv2.putText(blur2, "Circle" + str(count), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
                count += 1
        # Display detected circles
        cv2.imshow("Frame", blur2)
        # Display parameter sliders
        cv2.imshow('preview', img)
        # Exit loop if Escape is pressed
        if cv2.waitKey(1) == 27:
            break
    # Save parameter settings to global settings for use in game single captures
    param1 = cv2.getTrackbarPos("param1", 'preview')
    param2 = cv2.getTrackbarPos("param2", 'preview')
    minRadius = cv2.getTrackbarPos("minRadius", 'preview')
    maxRadius = cv2.getTrackbarPos("maxRadius", 'preview')

    # Release webcam capture
    cap.release()
    # Close windows
    cv2.destroyAllWindows()

def single_detection():

    # Make and safe shot of webcam
    cap = cv2.VideoCapture(3)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    output = cap.read()[1]
    grey = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(grey, (25, 25), cv2.BORDER_DEFAULT)
    blur2 = cv2.GaussianBlur(blur1, (25, 25), cv2.BORDER_DEFAULT)
    blur3 = cv2.bilateralFilter(blur2, 9, 75, 75)
    circles = cv2.HoughCircles(blur3, cv2.HOUGH_GRADIENT, 1.2, 100, param1=cv2.getTrackbarPos("param1", 'preview'), param2=cv2.getTrackbarPos("param2", 'preview'), minRadius=cv2.getTrackbarPos("minRadius", 'preview'), maxRadius=cv2.getTrackbarPos("maxRadius", 'preview'))
    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')
        count = 1
        for i in circles:
            # draw the circle in the output image, then draw a rectangle in the image
            # corresponding to the center of the circle
            cv2.circle(blur2, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(blur2, (i[0], i[1]), 2, (0, 0, 255), 3)
            cv2.putText(blur2, "Circle" + str(count), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
            count += 1

    # Display detected circles
    cv2.imshow("Frame", blur2)

cap.release()
cv2.destroyAllWindows()

# Keyboard control
while True:
    keyboard.wait('space')
    print('Detecting discs...')
    continuous_detection()


