"""
AI Canvas - Touchless Gesture Drawing
A beginner-friendly Python project using OpenCV and MediaPipe.

Controls:
  Pinch thumb + index finger to draw.
  Separate fingers to stop drawing.
  Press c to clear the canvas.
  Press u to undo the last stroke.
  Press e to toggle eraser.
  Press 1, 2, 3, 4 to change brush color.
  Press + or - to change brush size.
  Press s to save your drawing.
  Press q or ESC to quit.
"""

import os
import time
from collections import deque

import cv2
import mediapipe as mp
import numpy as np


# -------------------- SETTINGS --------------------
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

BRUSH_SIZE = 8
ERASER_SIZE = 35
PINCH_THRESHOLD = 0.055  # Increase slightly if pinch is hard to detect.

COLORS = {
    "cyan": (220, 220, 20),
    "green": (70, 220, 90),
    "pink": (220, 70, 220),
    "white": (245, 245, 245),
}
COLOR_KEYS = {
    ord("1"): "cyan",
    ord("2"): "green",
    ord("3"): "pink",
    ord("4"): "white",
}


def distance(point_a, point_b):
    """Return the straight-line distance between two (x, y) points."""
    return float(np.linalg.norm(np.array(point_a) - np.array(point_b)))


def draw_hud(frame, color_name, brush_size, eraser_on, pinch_on, fps):
    """Draw the instructions and current settings on the camera image."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (12, 12), (620, 148), (12, 20, 34), -1)
    cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)

    mode = "ERASER" if eraser_on else f"BRUSH: {color_name.upper()}"
    gesture = "DRAWING" if pinch_on else "PINCH TO DRAW"
    lines = [
        ("AI CANVAS  |  PYTHON + OPENCV + MEDIAPIPE", (80, 235, 220)),
        (f"{mode}   |   SIZE: {brush_size}   |   {gesture}", (245, 245, 245)),
        ("1-4: COLOR   E: ERASER   +/-: SIZE   U: UNDO", (190, 205, 220)),
        ("C: CLEAR   S: SAVE   Q: QUIT", (190, 205, 220)),
    ]

    y = 39
    for text, color in lines:
        cv2.putText(frame, text, (28, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, color, 1, cv2.LINE_AA)
        y += 31

    cv2.putText(frame, f"FPS: {fps:.0f}", (frame.shape[1] - 120, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 235, 220), 2,
                cv2.LINE_AA)


def main():
    global BRUSH_SIZE

    print("Starting AI Canvas...")
    print("If the webcam does not open, change CAMERA_INDEX to 1 in main.py.")

    # Open the laptop webcam.
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        print("Check camera permission and close other apps using the camera.")
        return

    # The drawing is stored on a separate, blank image.
    canvas = None
    previous_point = None
    current_color_name = "cyan"
    eraser_on = False
    pinch_on = False

    # Save one image per completed stroke for undo.
    undo_stack = []
    stroke_snapshot = None
    was_drawing = False

    # MediaPipe Hands finds 21 landmarks on each hand.
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    fps = 0.0
    previous_time = time.time()

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        ) as hands:

            while True:
                success, frame = camera.read()
                if not success:
                    print("Could not read a frame from the webcam.")
                    break

                # Mirror the image so it feels like looking in a mirror.
                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]

                if canvas is None:
                    canvas = np.zeros_like(frame)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                pinch_on = False
                hand_found = False

                if results.multi_hand_landmarks:
                    hand_found = True
                    hand_landmarks = results.multi_hand_landmarks[0]

                    # Draw the hand skeleton on the camera preview.
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    # Landmark 4 = thumb tip; landmark 8 = index fingertip.
                    thumb = hand_landmarks.landmark[4]
                    index = hand_landmarks.landmark[8]

                    thumb_point = (int(thumb.x * width), int(thumb.y * height))
                    index_point = (int(index.x * width), int(index.y * height))

                    pinch_distance = distance(
                        (thumb.x, thumb.y), (index.x, index.y)
                    )
                    pinch_on = pinch_distance < PINCH_THRESHOLD

                    # Show the tracked index fingertip.
                    cv2.circle(frame, index_point, 10, (0, 255, 255), -1)

                    if pinch_on:
                        if not was_drawing:
                            # Save the canvas before a new stroke starts.
                            undo_stack.append(canvas.copy())
                            if len(undo_stack) > 15:
                                undo_stack.pop(0)
                            stroke_snapshot = canvas.copy()

                        point = index_point
                        thickness = ERASER_SIZE if eraser_on else BRUSH_SIZE
                        color = (0, 0, 0) if eraser_on else COLORS[current_color_name]

                        if previous_point is not None:
                            # Smooth the line by drawing between consecutive points.
                            cv2.line(canvas, previous_point, point, color,
                                     thickness, cv2.LINE_AA)

                        previous_point = point
                        was_drawing = True
                    else:
                        previous_point = None
                        was_drawing = False

                else:
                    previous_point = None
                    was_drawing = False

                # Blend the transparent-looking drawing canvas over the camera.
                # Black pixels mean "no drawing"; colored pixels are drawn strokes.
                gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)
                inverse_mask = cv2.bitwise_not(mask)
                camera_part = cv2.bitwise_and(frame, frame, mask=inverse_mask)
                drawing_part = cv2.bitwise_and(canvas, canvas, mask=mask)
                combined = cv2.add(camera_part, drawing_part)

                # Display a small hint if no hand is visible.
                if not hand_found:
                    cv2.putText(combined, "Show one hand to the camera",
                                (25, height - 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (80, 235, 220), 2, cv2.LINE_AA)

                current_time = time.time()
                elapsed = current_time - previous_time
                if elapsed > 0:
                    fps = 1.0 / elapsed
                previous_time = current_time

                draw_hud(combined, current_color_name, BRUSH_SIZE,
                         eraser_on, pinch_on, fps)

                cv2.imshow("AI Canvas - Gesture Drawing", combined)
                key = cv2.waitKey(1) & 0xFF

                # Keyboard controls.
                if key == ord("q") or key == 27:
                    break
                elif key == ord("c"):
                    canvas[:] = 0
                    previous_point = None
                    was_drawing = False
                elif key == ord("u"):
                    if undo_stack:
                        canvas = undo_stack.pop()
                    previous_point = None
                    was_drawing = False
                elif key == ord("e"):
                    eraser_on = not eraser_on
                elif key in COLOR_KEYS:
                    current_color_name = COLOR_KEYS[key]
                    eraser_on = False
                elif key in (ord("+"), ord("=")):
                    BRUSH_SIZE = min(40, BRUSH_SIZE + 2)
                elif key in (ord("-"), ord("_")):
                    BRUSH_SIZE = max(2, BRUSH_SIZE - 2)
                elif key == ord("s"):
                    os.makedirs("saved_drawings", exist_ok=True)
                    filename = time.strftime(
                        "saved_drawings/ai_canvas_%Y%m%d_%H%M%S.png"
                    )
                    cv2.imwrite(filename, canvas)
                    print(f"Drawing saved to: {filename}")

    except Exception as error:
        print("\nSomething went wrong:", error)
        print("Check the installation instructions in README.md.")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("AI Canvas closed. Thank you!")


if __name__ == "__main__":
    main()
