import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Performance optimization
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

# Initialize MediaPipe (2 hands)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# CONFIGURATION
SMOOTH_FACTOR = 5 
curr_x, curr_y = 0, 0
prev_x, prev_y = 0, 0
FRAME_MARGIN = 80 

# Scroll parameters
SCROLL_SENSITIVITY = 18 
SCROLL_THRESHOLD = 5 

# CLICK THRESHOLDS
PINCH_THRESHOLD = 0.035 
SEPARATION_THRESHOLD = 0.06 

# EXIT GESTURE CONFIG
exit_counter = 0
EXIT_FRAMES_REQUIRED = 20 # Require ~1 second of holding the cross

# State flags
left_clicked = False
right_clicked = False

def get_distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
