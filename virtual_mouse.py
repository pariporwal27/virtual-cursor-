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
        
        cross_detected_this_frame = False
        
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            
            for hand_lms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

            # --- EXIT CROSS LOGIC ---
            if num_hands == 2:
                hand1_lms = results.multi_hand_landmarks[0]
                hand2_lms = results.multi_hand_landmarks[1]
                if is_finger_up(hand1_lms, 8) and is_finger_up(hand2_lms, 8):
                    tip1 = hand1_lms.landmark[8]
                    tip2 = hand2_lms.landmark[8]
                    if get_distance(tip1, tip2) < 0.04:
                        cross_detected_this_frame = True
            
            # --- MAIN CONTROL LOGIC ---
            if num_hands == 1 or (num_hands == 2 and not cross_detected_this_frame):
                hand_landmarks = results.multi_hand_landmarks[0]
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                
                index_up = is_finger_up(hand_landmarks, 8)
                middle_up = is_finger_up(hand_landmarks, 12)
                
                target_x = np.interp(index_tip.x * w, (FRAME_MARGIN, w - FRAME_MARGIN), (0, screen_width))
                target_y = np.interp(index_tip.y * h, (FRAME_MARGIN, h - FRAME_MARGIN), (0, screen_height))
                curr_x = prev_x + (target_x - prev_x) / SMOOTH_FACTOR
                curr_y = prev_y + (target_y - prev_y) / SMOOTH_FACTOR
                
                if index_up and middle_up:
                    dy = curr_y - prev_y
                    if abs(dy) > SCROLL_THRESHOLD:
                        pyautogui.scroll(-int(dy * SCROLL_SENSITIVITY))
                    cv2.putText(img, "SCROLLING", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                elif index_up:
                    pyautogui.moveTo(curr_x, curr_y)
                    cv2.putText(img, "MOVING", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                
                d_index = get_distance(index_tip, thumb_tip)
                d_middle = get_distance(middle_tip, thumb_tip)
                
                if d_index < PINCH_THRESHOLD and d_middle > SEPARATION_THRESHOLD:
                    if not left_clicked:
                        pyautogui.click()
                        left_clicked = True
                    cv2.circle(img, (int(index_tip.x * w), int(index_tip.y * h)), 25, (0, 255, 0), cv2.FILLED)
                else: left_clicked = False
                    
                if d_middle < PINCH_THRESHOLD and d_index > SEPARATION_THRESHOLD:
                    if not right_clicked:
                        pyautogui.rightClick()
                        right_clicked = True
                    cv2.circle(img, (int(middle_tip.x * w), int(middle_tip.y * h)), 25, (0, 0, 255), cv2.FILLED)
                else: right_clicked = False
                
                prev_x, prev_y = curr_x, curr_y

        if cross_detected_this_frame:
            exit_counter += 1
            progress = int((exit_counter / EXIT_FRAMES_REQUIRED) * 100)
            cv2.putText(img, f"EXITING... {progress}%", (w//2 - 100, h//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            exit_counter = max(0, exit_counter - 1)
            
        if exit_counter >= EXIT_FRAMES_REQUIRED:
            break
            
        cv2.imshow(window_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
