# AI Canvas — Python Gesture-Controlled Drawing

A beginner-friendly AI/Computer Vision project. It uses your webcam to track your hand and lets you draw by pinching your thumb and index finger together.

## What you will learn

- Python basics: variables, functions, loops and conditions
- OpenCV: webcam video and image drawing
- MediaPipe: hand landmark detection
- NumPy: coordinate distance calculations
- Computer Vision and Human-Computer Interaction

## Requirements

- Windows, macOS or Linux laptop
- Python 3.10 or 3.11 (recommended)
- VS Code
- Working webcam
- Internet connection for package installation

## 1. Open the project

1. Download and extract `AI-Canvas-Python.zip`.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Select the extracted `AI-Canvas-Python` folder.

## 2. Create a virtual environment

Open **Terminal → New Terminal** in VS Code.

Windows:
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

If `py -3.11` is not available, try:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

If activation is blocked in Windows PowerShell, run this in the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Then activate the environment again.

## 3. Install the libraries

With the virtual environment activated, run:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Run the application

```bash
python main.py
```

Allow webcam access if your computer asks. Hold one hand in view. Pinch your thumb and index fingertip together and move your hand to draw. Separate them to stop drawing.

## Controls

| Key | Action |
|---|---|
| `1` | Cyan brush |
| `2` | Green brush |
| `3` | Pink brush |
| `4` | White brush |
| `e` | Toggle eraser |
| `+` or `=` | Increase brush size |
| `-` | Decrease brush size |
| `u` | Undo last stroke |
| `c` | Clear canvas |
| `s` | Save drawing |
| `q` or `Esc` | Quit |

Saved images are placed in the `saved_drawings` folder.

## How the gesture works

MediaPipe detects 21 landmarks on the hand:
- Landmark 4 is the thumb tip.
- Landmark 8 is the index fingertip.

The program measures the distance between these fingertips. If the distance is smaller than a threshold, the program draws at the index fingertip position.

If pinching is difficult to detect, open `main.py` and change:
```python
PINCH_THRESHOLD = 0.055
```
Try `0.065` or `0.075`.

## Troubleshooting

### `python` is not recognized
Install Python 3.11 from https://www.python.org/downloads/ and select **Add Python to PATH** during installation. Restart VS Code.

### No module named cv2 / mediapipe
Activate `.venv` and run:
```bash
python -m pip install -r requirements.txt
```

### Webcam will not open
- Close Zoom, Teams or other apps using the camera.
- Check camera permission in your operating system.
- In `main.py`, change `CAMERA_INDEX = 0` to `CAMERA_INDEX = 1` and try again.

### Installation errors
Use 64-bit Python 3.10 or 3.11. These pinned package versions are intended for those Python versions.

## Project structure

```text
AI-Canvas-Python/
├── main.py
├── requirements.txt
└── README.md
```

## Privacy note

This program processes webcam frames locally on your computer. It does not contain code to upload or store webcam video. Only drawings you explicitly save with the `s` key are written to disk.
