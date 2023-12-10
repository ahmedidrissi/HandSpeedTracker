import HandSpeedTracker as hst
import cv2
import tkinter as tk
from tkinter import filedialog
import os

# Create a window
window = tk.Tk()
window.title("Hand Speed Tracker")
window.geometry("500x150")  # Adjusted the height
window.configure(bg="#f0f0f0")  # Light gray background
window.resizable(False, False)  # Disable window resizing

# Create a label
label_info = tk.Label(window, text="Hand Speed Tracker", font=("Arial", 24), bg="#f0f0f0")
label_info.grid(row=0, column=0, columnspan=6, sticky="nsew", pady=20)

# Create a button
button_choose_file = tk.Button(window, text="Choose a video file", font=("Arial", 16), bg="#4caf50", fg="white", command=lambda: choose_video_file())
button_choose_file.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=20, pady=20)


# Adjust grid weights to make the button and label centered
window.rowconfigure([0, 1], weight=1)
window.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)

def choose_video_file():
    # get the path of the video file
    video_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a video file", filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    # get the name of the video file without the extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    # create a video capture object
    cap = cv2.VideoCapture(video_path)
    # fix the width and height of the video to 640 and 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # set the frame rate to 30
    cap.set(cv2.CAP_PROP_FPS, 30)

    hand_speed_tracker = hst.HandSpeedTracker()
    speed_list = {
        "left_hand": [],
        "right_hand": []
    }
    while cap.isOpened():
        success, image = cap.read() # reading the image from the webcam
        if not success:
            print("Ignoring empty video frame.")
            continue
        
        image, coordinates = hand_speed_tracker.find_hands(image)
        left_hand_speed = hand_speed_tracker.calculate_speed(coordinates["left_hand"])
        right_hand_speed = hand_speed_tracker.calculate_speed(coordinates["right_hand"])
        speed_list["left_hand"].append(left_hand_speed)
        speed_list["right_hand"].append(right_hand_speed)
        cv2.imshow("Hand Tracker", image)

        key = cv2.waitKey(1)
        if key == ord('s'):
            hand_speed_tracker.plot_speed(speed_list["left_hand"], "left", video_name)
            hand_speed_tracker.plot_speed(speed_list["right_hand"], "right", video_name)
            hand_speed_tracker.save_results(video_name + ".xlsx", coordinates, speed_list)
            hand_speed_tracker.close()
            cap.release()
            cv2.destroyAllWindows()
            break

def quit():
    window.quit()
    window.destroy()

# Bind the window with the quit function
window.protocol("WM_DELETE_WINDOW", quit)

# Run the window
window.mainloop()