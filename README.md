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
