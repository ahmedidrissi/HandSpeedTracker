import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import pandas as pd

class HandSpeedTracker:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_drawing = mp.solutions.drawing_utils # to draw the landmarks
        self.mp_drawing_styles = mp.solutions.drawing_styles 
        self.mp_hands = mp.solutions.hands # to detect the hands

        self.hands = self.mp_hands.Hands() # creating a hands object

        # dictionary to store the coordinates of the landmarks
        self.coordinates = {
                "left_hand": [], # list of tuples (x, y, z)
                "right_hand": [] # list of tuples (x, y, z)
            }

    def find_hands(self, image):
        # Flip the image horizontally
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # Store the results in the results variable
        results = self.hands.process(image)

        # Looping through the results variable to get the landmarks coordinates
        left_hand = None
        right_hand = None
        left_hand_index = None
        right_hand_index = None
        if results.multi_hand_landmarks:

            # Get the left and right hand landmarks
            if len(results.multi_hand_landmarks) == 1:
                # draw the landmarks on one hand
                self.mp_drawing.draw_landmarks(image, results.multi_hand_landmarks[0], self.mp_hands.HAND_CONNECTIONS, self.mp_drawing_styles.get_default_hand_landmarks_style(), self.mp_drawing_styles.get_default_hand_connections_style())
                if results.multi_handedness[0].classification[0].label == "Left":
                    left_hand = results.multi_hand_landmarks[0]
                    right_hand = None
                else:
                    left_hand = None
                    right_hand = results.multi_hand_landmarks[0]
            else:
                # draw the landmarks on both hands
                self.mp_drawing.draw_landmarks(image, results.multi_hand_landmarks[0], self.mp_hands.HAND_CONNECTIONS, self.mp_drawing_styles.get_default_hand_landmarks_style(), self.mp_drawing_styles.get_default_hand_connections_style())
                self.mp_drawing.draw_landmarks(image, results.multi_hand_landmarks[1], self.mp_hands.HAND_CONNECTIONS, self.mp_drawing_styles.get_default_hand_landmarks_style(), self.mp_drawing_styles.get_default_hand_connections_style())
                if results.multi_handedness[0].classification[0].label == "Left":
                    left_hand = results.multi_hand_landmarks[0]
                    right_hand = results.multi_hand_landmarks[1]

            # Get the left hand landmark and draw a blue circle  
            if left_hand:
                x_left, y_left, z_left = left_hand.landmark[8].x, left_hand.landmark[8].y, left_hand.landmark[8].z
                self.coordinates["left_hand"].append((x_left, y_left, z_left))
                cv2.circle(image, (int(x_left * image.shape[1]), int(y_left * image.shape[0])), 10, (255, 0, 0), -1)

            # Get the right hand landmark and draw a red circle
            if right_hand:
                x_right, y_right, z_right = right_hand.landmark[8].x, right_hand.landmark[8].y, right_hand.landmark[8].z
                self.coordinates["right_hand"].append((x_right, y_right, z_right))
                cv2.circle(image, (int(x_right * image.shape[1]), int(y_right * image.shape[0])), 10, (0, 0, 255), -1)

            # If one hand is detected, the coordinates of the other hand are set to a list of null values
            if left_hand and not right_hand:
                self.coordinates["right_hand"].append((0, 0, 0))
            elif right_hand and not left_hand:
                self.coordinates["left_hand"].append((0, 0, 0))            

        # if no hands are detected, the coordinates are set to a list of null values
        else:
            self.coordinates["left_hand"].append((0, 0, 0))
            self.coordinates["right_hand"].append((0, 0, 0))
                
        # Flip the image back
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        return image, self.coordinates
    
    def close(self):
        self.hands.close()

    # function to calculate the speed of the hand based on the coordinates of a landmark
    def calculate_speed(self, coordinates):
        # coordinates is a list of tuples (x, y, z)
        # the speed is calculated by dividing the distance between the last two coordinates by the time difference between the last two coordinates
        if len(coordinates) < 2:
            return 0
        else:
            x1, y1, z1 = coordinates[-2]
            x2, y2, z2 = coordinates[-1]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
            time_difference = 1 
            return distance / time_difference
        
    # function to plot the speed of both hands
    def plot_speed(self, speed_list, name):
        plt.title("Speed of the hands - " + name)
        plt.xlabel("Time")
        plt.ylabel("Speed")
        plt.plot(speed_list["left_hand"], label="Left hand")
        plt.plot(speed_list["right_hand"], label="Right hand")
        plt.legend()
        plt.savefig(name + ".png")
        plt.show()

    # function to save the coordinates and speed of left and right hand in an excel file
    def save_results(self, file_name, coordinates, speed_list):
        # coordinates is a dictionary with the keys "left_hand" and "right_hand"
        # speed_list is a dictionary with the keys "left_hand" and "right_hand"
        
        # create a dataframe
        df1 = pd.DataFrame(coordinates["left_hand"], columns=["x_left", "y_left", "z_left"])
        df2 = pd.DataFrame(speed_list["left_hand"], columns=["speed_left"])
        df3 = pd.DataFrame(coordinates["right_hand"], columns=["x_right", "y_right", "z_right"])
        df4 = pd.DataFrame(speed_list["right_hand"], columns=["speed_right"])
        df = pd.concat([df1, df2, df3, df4], axis=1)
        # save the dataframe in an excel file
        df.to_excel(file_name, index=False)