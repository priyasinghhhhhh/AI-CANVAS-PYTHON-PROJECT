🎨 AI Canvas Drawing Project

Draw in the Air Using Hand Gestures – An AI-Powered Virtual Canvas

📌 About the Project

AI Canvas Drawing is an interactive computer vision project that allows users to draw on a virtual canvas using hand gestures in front of a webcam.

Instead of using a traditional mouse, keyboard, or touchscreen, users can move their fingers in the air to create digital drawings.

The project uses AI-based hand tracking and computer vision to detect hand movements and convert them into drawing actions in real time.

✨ Features

- 🖐️ Real-time hand detection.
- 🎨 Draw using finger movements.
- 🌈 Multiple drawing colors.
- 🧹 Eraser functionality.
- ✏️ Virtual drawing canvas.
- 📷 Live webcam tracking.
- 🤖 AI-powered hand gesture recognition.
- ⚡ Interactive and user-friendly interface.

🛠️ Technologies Used

Technology| Purpose
Python| Main programming language
OpenCV| Image processing and webcam access
MediaPipe| Hand landmark detection
NumPy| Canvas and image operations
Streamlit (optional)| Web interface

📁 Project Structure

AI-Canvas-Draw/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── hand_tracking.py
│   └── drawing.py
│
├── assets/
│   └── screenshots/
│
└── output/
    └── drawings/

⚙️ Installation and Setup

1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Navigate to the Project Folder

cd AI-Canvas-Draw

3. Install Required Libraries

pip install -r requirements.txt

4. Run the Project

python app.py

Allow webcam access when prompted.

🎮 How to Use

1. Start the application.
2. Allow webcam access.
3. Show your hand in front of the camera.
4. Move your index finger to draw.
5. Select different colors to change drawing styles.
6. Use the eraser to remove unwanted drawings.
7. Save your artwork.

🧠 How It Works

1. Webcam Input: Captures live video using OpenCV.
2. Hand Detection: MediaPipe detects hand landmarks.
3. Gesture Recognition: Identifies finger positions and gestures.
4. Drawing Logic: Converts finger movements into canvas strokes.
5. Display Output: Shows the drawing in real time.

🚀 Future Enhancements

- AI-based shape recognition.
- Voice-controlled drawing.
- Multiple brush styles and sizes.
- Gesture-based color selection.
- Save drawings as PNG or JPG.
- Hand gesture shortcuts.
- AI-powered sketch-to-image generation.

🎓 Learning Outcomes

- Python programming.
- Computer vision.
- Hand landmark detection.
- Image processing.
- Gesture recognition.
- Real-time AI applications.

📌 Project Information

Project Name: AI Canvas Drawing

Category: Artificial Intelligence / Computer Vision

Language: Python

Level: Beginner to Intermediate

📜 License

This project is created for educational and learning purposes.

---

"Turn your hand movements into digital art. Create without touching the screen!" 🎨
