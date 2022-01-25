import cv2
import numpy as np
import keyboard

# Default Hough Circle Detection parameters
param1 = 28
param2 = 50
minRadius = 20
maxRadius = 135

# Define which webcam input you use
webcam = 0

# Definitions for Logitech HD720
board_size = 720
offset = 1280/4-30

def continuous_detection():

    # Print slider values
    def print_bar(x):
        pass

    # Open webcam and set video size
    cap = cv2.VideoCapture(webcam)
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
                cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
                cv2.putText(output, "Circle" + str(count), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
                count += 1
        add_grid(8, output, offset)
        # Display detected circles
        cv2.imshow("Frame", output)
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

    # Open webcam capture
    cap = cv2.VideoCapture(webcam)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    output = cap.read()[1]
    grey = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(grey, (25, 25), cv2.BORDER_DEFAULT)
    blur2 = cv2.GaussianBlur(blur1, (25, 25), cv2.BORDER_DEFAULT)
    blur3 = cv2.bilateralFilter(blur2, 9, 75, 75)
    circles = cv2.HoughCircles(blur3, cv2.HOUGH_GRADIENT, 1.2, 100, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')
        count = 1
        for i in circles:
            # draw the circle in the output image, then draw a rectangle in the image
            # corresponding to the center of the circle
            cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
            cv2.putText(output, "Circle" + str(count), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
            print("Circle " + str(count) + " X: " + str(i[0]) + " Y: " + str(i[1]))
            count += 1
    # Display detected circles
    cv2.imshow("Frame", output)
    # Wait for keypress to close window
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

# Overlay a grid of lines representing the checker board, can be used to align the camera
# Takes grid size (IxI), input image and offset to center the board on the image
def add_grid(size, input, offset):
    for i in range(9):
        cv2.line(input, (int(((board_size / size) * i)+offset), 0), (int(((board_size / size) * i)+offset), board_size), (0, 0, 255), 3, 3)
        cv2.line(input, (int(offset), int((board_size / size) * i)), (int(board_size+offset), int((board_size / size) * i)), (0, 0, 255), 3, 3)

# Keyboard control
while True:
    if keyboard.is_pressed('space'):
        print('\nDetecting discs...')
        continuous_detection()
    elif keyboard.is_pressed('s'):
        print("\nTaking snapshot")
        single_detection()




