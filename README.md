# Hand Speed Tracker

## Description
This is a simple program that tracks the speed of both hands based on a video file. It uses the [MediaPipe](https://google.github.io/mediapipe/) library to detect the hands and the [OpenCV](https://opencv.org/) library to read the video file and display the results. The program also uses the [Matplotlib](https://matplotlib.org/) library to display the results in a graph. The coordinates of the hands are saved in an Excel file using the [Pandas](https://pandas.pydata.org/) library and the [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/) library. I used Tkinter to create a simple GUI for the program that allows the user to select the video file.

## How to use
1. Download the repository
2. Install the required packages
    - `pip install mediapipe`
    - `pip install opencv-python`
    - `pip install matplotlib`
    - `pip install pandas`
    - `pip install openpyxl`
3. Run the program
