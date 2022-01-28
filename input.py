import cv2
import numpy as np
import keyboard
from constants import ROWS

class Input:
    def __int__(self):
        pass

    # Default Hough Circle Detection parameters
    param1 = 28
    param2 = 50
    minRadius = 20
    maxRadius = 135

    # Checkerboard parameter
    size = ROWS
    squares = size * size

    # Define which webcam input you use
    webcam = 0
    webcam_width = 1280
    webcam_height = 720

    # Definitions for Logitech HD720
    board_size = 720
    offset = 1280/4-30

    # Create dictionary for board state
    board = {}
    for x in range(size):
        for y in range(size):
            board[x, y] = 0

    def continuous_detection(self):

        # Print slider values
        def print_bar(x):
            pass

        # Open webcam and set video size
        cap = cv2.VideoCapture(self.webcam)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.webcam_height)

        # Parameter settings window
        img = np.zeros((300, 300, 3), np.uint8)
        cv2.namedWindow("preview")
        #   Sliders
        cv2.createTrackbar('param1', "preview", 28, 500, print_bar)
        cv2.createTrackbar('param2', "preview", 50, 500, print_bar)
        cv2.createTrackbar('minRadius', "preview", 20, 500, print_bar)
        cv2.createTrackbar('maxRadius', "preview", 135, 500, print_bar)

        while cap.isOpened():
            # Read webcam input
            output = cap.read()[1]
            # FOR DEVELOPMENT
            # output = cv2.imread('webcam-image.png')
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
            # Use add_grid method to display a checkers grid over the webcam input
            self.add_grid(8, output, self.offset)
            # Use check_grid method to check if circles are inside of grid square
            self.check_grid(8, output, self.offset, circles)
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

    def single_detection(self):

        # Open webcam capture
        cap = cv2.VideoCapture(self.webcam)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.webcam_height)

        output = cap.read()[1]
        grey = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.GaussianBlur(grey, (25, 25), cv2.BORDER_DEFAULT)
        blur2 = cv2.GaussianBlur(blur1, (25, 25), cv2.BORDER_DEFAULT)
        blur3 = cv2.bilateralFilter(blur2, 9, 75, 75)
        circles = cv2.HoughCircles(blur3, cv2.HOUGH_GRADIENT, 1.2, 100, param1=self.param1, param2=self.param2, minRadius=self.minRadius, maxRadius=self.maxRadius)
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
        self.check_grid(8, output, self.offset, circles)
        # print(self.board)
        # Display detected circles
        # cv2.imshow("Frame", output)
        # Wait for keypress to close window
        # cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()

    def save(self):
        # Open webcam capture
        cap = cv2.VideoCapture(self.webcam)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.webcam_height)

        image = cap.read()[1]
        cv2.imwrite('webcam-image.png', image)
        print("Saved image.")
        cap.release()

    # Overlay a grid of lines representing the checker board, can be used to align the camera
    # Takes grid size (IxI), input image and offset to center the board on the image
    def add_grid(self, size, input, offset):
        grid_size = self.board_size/size
        # Draw board over webcam view
        for i in range(size+1):
            cv2.line(input, (int(((self.board_size / size) * i)+offset), 0), (int(((self.board_size / size) * i)+offset), self.board_size), (0, 0, 255), 3, 3)
            cv2.line(input, (int(offset), int((self.board_size / size) * i)), (int(self.board_size+offset), int((self.board_size / size) * i)), (0, 0, 255), 3, 3)
        # Add square numbers on the board
        for x in range(size):
            for y in range(size):
                count = y + size * x
                cv2.putText(input, str(count), (int((grid_size/2-20) + offset + (grid_size*x)), int(60 + grid_size*y)), cv2.FONT_HERSHEY_COMPLEX, 1.1, (255, 255, 255), 2)


    # Check if a circle is inside of the checker board grid
    def check_grid(self, size, input, offset, circles):
        grid_size = self.board_size/size
        if circles is not None:
            # For every detected circle
            for i in circles:
                # Scan across grid in x and y direction according to size of grid
                for x in range(size):
                    col = x
                    for y in range(size):
                        row = y
                        # Define starting position of first square in the grid then build from there
                        start_pos_x = offset
                        end_pos_x = offset + grid_size
                        start_pos_y = 0
                        end_pos_y = grid_size
                        count = y + size * x
                        # For every square in the grid move detection statement by the step size of the grid
                        if i[0] > start_pos_x+(grid_size*x) and i[0] < end_pos_x + (grid_size*x) and i[1] > start_pos_y + (grid_size*y) and i[1] < end_pos_y + (grid_size*y):
                            # Draw a green highlight over a square that has a circle in it
                            cv2.rectangle(input, (int(start_pos_x + (grid_size*x)), int(grid_size*y), int(grid_size), int(grid_size)), (0, 255, 0), 3)
                            # Update board dictionary accordingly
                            self.board[col, row] = 1
                            print("Square: " + str(count) + " Col: " + str(col) + " Row: " + str(row))
                        else:
                            # If no circle is detected within a board square update the board dictionary accordingly
                            self.board[col, row] = 0

    # # Keyboard control
    # while True:
    #     if keyboard.is_pressed('space'):
    #         print('\nStarting continuous detection...')
    #         continuous_detection()
    #     elif keyboard.is_pressed('s'):
    #         print("\nStarting single detection...")
    #         single_detection()
    #     elif keyboard.is_pressed('w'):
    #         print("\nSaving image from webcam...")
    #         save()




