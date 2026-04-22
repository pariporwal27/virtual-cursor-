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

def is_finger_up(hand_landmarks, finger_index):
    mcp_y = hand_landmarks.landmark[finger_index - 3].y
    tip_y = hand_landmarks.landmark[finger_index].y
    return tip_y < mcp_y

def main():
    global curr_x, curr_y, prev_x, prev_y, left_clicked, right_clicked, exit_counter
    
    cap = cv2.VideoCapture(0)
    
    window_name = "Virtual Mouse - Robust Exit"
    cv2.namedWindow(window_name)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    
    while cap.isOpened():
        success, img = cap.read()
        if not success: break
            
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            # --- MAIN CONTROL LOGIC ---
            hand_landmarks = results.multi_hand_landmarks[0]
            index_tip = hand_landmarks.landmark[8]
            
            # Mapping coordinates to screen size
            target_x = np.interp(index_tip.x * w, (FRAME_MARGIN, w - FRAME_MARGIN), (0, screen_width))
            target_y = np.interp(index_tip.y * h, (FRAME_MARGIN, h - FRAME_MARGIN), (0, screen_height))
        
        cv2.imshow(window_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
