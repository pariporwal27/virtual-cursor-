# VisionCursor: AI-Powered Virtual Mouse

VisionCursor is a robust, vision-based Human-Computer Interface (HCI) that allows users to control their computer cursor, perform clicks, and scroll using simple hand gestures via a standard webcam. Powered by **MediaPipe** and **OpenCV**, it provides a touchless and intuitive way to interact with your digital environment.

## 🚀 Key Features
- **Smooth Cursor Movement**: Real-time tracking with linear interpolation for jitter-free movement.
- **Pinch-to-Click**: Perform left and right clicks using natural pinch gestures.
- **Gesture-Based Scrolling**: Scroll through documents and web pages by raising two fingers.
- **Robust Exit Gesture**: Securely exit the application by crossing your index fingers for 1 second.
- **Visual Feedback**: Real-time on-screen overlays for gesture recognition status.

## 🛠️ Tech Stack
- **Python**: Core logic and automation.
- **OpenCV**: Image processing and camera stream handling.
- **MediaPipe**: High-fidelity hand landmark detection and tracking.
- **PyAutoGUI**: Cross-platform mouse and keyboard automation.
- **NumPy**: Efficient coordinate and distance calculations.

## 📋 Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.8 or higher
- A standard Webcam
- Active internet connection (for initial MediaPipe model downloads)

## 🔧 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/pariporwal27/virtual-cursor-.git
   cd virtual-cursor-
   ```

2. **Install required dependencies:**
   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

## 🎮 Usage
1. Run the script:
   ```bash
   python virtual_mouse.py
   ```
2. **Move Cursor**: Raise your index finger and move it within the camera frame.
3. **Left Click**: Pinch your index finger and thumb together.
4. **Right Click**: Pinch your middle finger and thumb together.
5. **Scroll**: Raise both index and middle fingers and move them vertically.
6. **Exit**: Cross your index fingers and hold for 1 second, or press `q`.

## 📜 Future Enhancements
- Support for multi-monitor setups.
- Customizable gesture mappings.
- Low-light mode optimization.

---
Developed as a college project to explore Human-Computer Interaction through Computer Vision.
