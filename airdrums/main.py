"""
With PyGame
"""
import pygame
import cv2
import traceback
from detection import detect_circles
from threading import Thread


def check_collision(rect, circle):
    x, y, w, h = rect
    center_x, center_y, radius = circle

    # Check if the circle collides with the rectangle
    if center_x + radius < x or center_x - radius > x + w or \
       center_y + radius < y or center_y - radius > y + h:
        return False
    else:
        return True


# Initialize pygame mixer
pygame.mixer.init()

# Load sound files into separate channels
channel1 = pygame.mixer.Channel(0)
box_sound = pygame.mixer.Sound('sounds/caixa.mp3')


def play_beep():
    t = Thread(target=channel1.play, args=(box_sound,), daemon=True)
    t.start()


# Coordinates and dimensions of the rectangle
x_r = 400
y_r = 100
width_r = 100
height_r = 150

# Pygame initialization
pygame.init()

# Window dimensions
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))

# Camera initialization
camera = cv2.VideoCapture(0)
# Set webcam frame size
camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

tracker = cv2.legacy.TrackerCSRT_create()
multitracker = cv2.legacy.MultiTracker_create()
bboxes = []

NUM_TRACKED_OBJS = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close the window if the close button is pressed
            camera.release()
            pygame.quit()
            quit()

    # Capture frame from the camera
    ret, frame_bgr = camera.read()

    # Rotate the frame 90 degrees counterclockwise
    frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Convert the OpenCV image to Pygame format
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    if len(bboxes) == NUM_TRACKED_OBJS:
        # only tracker bboxes
        ...
    elif 0 < len(bboxes) < NUM_TRACKED_OBJS:
        # update tracker; detect circles; if new circle is detected add to tracker
        ...
    else:
        try:
            circles = detect_circles(frame_bgr=frame_bgr)
        except Exception:
            traceback.print_exc()
            circles = []

        for pt in circles:
            a, b, r = pt[0], pt[1], pt[2]
            pt1 = [(a - r), (b - r)]
            pt2 = [(a + r), (b + r)]

            # Draw the circumference of the circle.
            cv2.circle(frame_rgb, (a, b), 20, (0, 255, 0), 2)

    for pt in circles:
        a, b, r = pt[0], pt[1], pt[2]

        if check_collision(
            (x_r, y_r, width_r, height_r), (a, b, 20)
        ):
            play_beep()

        # Draw the circumference of the circle.
        cv2.circle(frame_rgb, (a, b), 20, (0, 255, 0), 2)

    # Draw the rectangle on the image
    cv2.rectangle(frame_rgb, (x_r, y_r), (x_r + width_r, y_r + height_r), (0, 0, 255), 2)

    frame_pygame = pygame.surfarray.make_surface(frame_rgb)

    # Display the frame on the Pygame window
    window.blit(frame_pygame, (0, 0))

    pygame.display.update()

    # Check if the 'Esc' key is pressed to exit the loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break

# Release resources
camera.release()
pygame.quit()
