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
