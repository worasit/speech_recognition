import cv2
import pygame
import os

# Initialize pygame
pygame.init()

# Load the pre-trained face and eye detection models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Get the full path to the sound file
current_dir = os.path.dirname(os.path.abspath(__file__))
sound_file = os.path.join(current_dir, 'system-notification.mp3')


# Function to detect faces and eyes, and play beep sound when blinking is detected
def detect_faces_and_eyes(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Get the region of interest (ROI) for eyes within the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Draw circles around the detected eyes
        for (ex, ey, ew, eh) in eyes:
            center = (x + ex + ew // 2, y + ey + eh // 2)
            radius = min(ew, eh) // 2
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            print('eh: ' + str(eh))
            # Check if the eye is closed (eyelid covers the eye)
            if eh > 200:
                # Play beep sound
                pygame.mixer.Sound(sound_file).play()

    return frame


# Function to capture video from the camera and detect faces, eyes, and blinking
def main():
    # Create a video capture object for the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Continuously capture frames from the camera and detect faces, eyes, and blinking
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Detect faces, eyes, and blinking in the frame
        frame_with_detection = detect_faces_and_eyes(frame)

        # Display the frame with detected faces, eyes, and blinking
        cv2.imshow('Face and Eye Detection with Blinking', frame_with_detection)

        # Check for 'q' key press to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
