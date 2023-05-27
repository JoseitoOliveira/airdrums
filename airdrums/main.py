"""
With PyGame
"""
import pygame
import cv2
import traceback
from detection import detectar_esfera_azul
from drum_element import DrumElement
from utils import FPSMedidor

# Initialize pygame mixer
pygame.mixer.init()

# Camera initialization
camera = cv2.VideoCapture(2)

window_width = 640
window_height = 480

# Coordinates and dimensions of the rectangle
drum_set = [
    DrumElement(
        'Snare',
        x=round(0.9 * window_height),
        y=round(0.4 * window_width),
        ax1=round(0.07 * window_height),
        ax2=round(0.12 * window_width),
        angle=0,
        sound='sounds/caixa.mp3'
    ),
    DrumElement(
        'Hi-hat',
        x=round(0.75 * window_height),
        y=round(0.2 * window_width),
        ax1=round(0.07 * window_height),
        ax2=round(0.12 * window_width),
        angle=-10,
        sound='sounds/chimbal.mp3'
    ),
    DrumElement(
        'Ride-Cymbal',
        y=round(0.9 * window_width),
        x=round(0.25 * window_height),
        ax1=round(0.15 * window_height),
        ax2=round(0.18 * window_width),
        angle=15,
        sound='sounds/prato.mp3'
    )
]

# Pygame initialization
pygame.init()

# Window dimensions
window = pygame.display.set_mode((window_width, window_height))


# # Set webcam frame size
camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

tracker = cv2.legacy.TrackerCSRT_create()
multitracker = cv2.legacy.MultiTracker_create()
bboxes = []

NUM_TRACKED_OBJS = 1

fps_medidor = FPSMedidor()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close the window if the close button is pressed
            camera.release()
            pygame.quit()
            quit()

    # Capture frame from the camera
    ret, frame_bgr = camera.read()

    if not ret:
        break

    # Rotate the frame 90 degrees counterclockwise
    frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Convert the OpenCV image to Pygame format
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    try:
        circles = detectar_esfera_azul(frame_bgr)
    except Exception:
        traceback.print_exc()
        circles = []

    for drum_ele in drum_set:
        drum_ele.interact_with_circles(circles)
        drum_ele.draw(frame_rgb)
        for c in circles:
            a, b, r = c[0], c[1], c[2]
        #     pt = drum_ele.ponto_mais_proximo(c)
        #     cv2.circle(frame_rgb, pt, 2, (255, 0, 0), 2)
        #     cv2.line(frame_rgb, pt, drum_ele.f1, (0, 0, 255), 1)
        #     cv2.line(frame_rgb, pt, drum_ele.f2, (0, 0, 255), 1)
            cv2.circle(frame_rgb, (a, b), r, (0, 255, 0), 2)

    if (fps := fps_medidor.update()) is not None:
        print(f'FPS:{fps}')

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
