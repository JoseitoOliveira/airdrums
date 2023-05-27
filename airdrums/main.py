"""
With pg
"""
import pygame as pg
import cv2
import traceback
from detection import detectar_esfera_azul
from drum_element import DrumElement
from utils import FPSMedidor

# Initialize pg mixer
pg.mixer.init()

# Camera initialization
camera = cv2.VideoCapture(2)

window_width = 800
window_height = 600

# Coordinates and dimensions of the rectangle
drum_set = [
    DrumElement(
        'Snare',
        x=round(0.9 * window_height),
        y=round(0.4 * window_width),
        d=round(0.8 * window_height),
        ax1=round(0.07 * window_height),
        ax2=round(0.12 * window_width),
        angle=0,
        sound='sounds/caixa.mp3'
    ),
    DrumElement(
        'Hi-hat',
        x=round(0.75 * window_height),
        y=round(0.2 * window_width),
        d=round(0.65 * window_height),
        ax1=round(0.07 * window_height),
        ax2=round(0.12 * window_width),
        angle=-10,
        sound='sounds/chimbal.mp3'
    ),
    DrumElement(
        'Ride-Cymbal',
        x=round(0.25 * window_height),
        y=round(0.9 * window_width),
        d=round(0.5 * window_height),
        ax1=round(0.15 * window_height),
        ax2=round(0.18 * window_width),
        angle=15,
        sound='sounds/prato.mp3'
    )
]

# pg initialization
pg.init()
top_view = pg.Surface((window_width, window_height))

# Window dimensions
window = pg.display.set_mode((window_width, window_height * 2))


# # Set webcam frame size
camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

tracker = cv2.legacy.TrackerCSRT_create()
multitracker = cv2.legacy.MultiTracker_create()

NUM_TRACKED_OBJS = 1
DISTANCIA_FOCAL = 36 # mm
TAMANHO_REAL = 50 # mm
D_MAX = 180
D_MIN = 20
H_MAX = 40
H_MIN = 20

fps_medidor = FPSMedidor()

while True:
    top_view.fill((241, 243, 244))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Close the window if the close button is pressed
            camera.release()
            pg.quit()
            quit()

    # Capture frame from the camera
    ret, frame_bgr = camera.read()

    if not ret:
        break

    # Rotate the frame 90 degrees counterclockwise
    frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Convert the OpenCV image to pg format
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    try:
        circles = detectar_esfera_azul(frame_bgr)
    except Exception:
        traceback.print_exc()
        circles = []

    for drum_ele in drum_set:
        drum_ele.interact_with_circles(circles)
        drum_ele.draw_front_opencv(frame_rgb)
        drum_ele.draw_top_pygame(top_view)
        for c in circles:
            a, b, r = c[0], c[1], c[2]
            d0 = (TAMANHO_REAL * DISTANCIA_FOCAL) / r
            d1 = round((d0 + D_MIN) * (window_width / (D_MAX - D_MIN)))
            h = round(H_MAX - (a / window_height) * (H_MAX - H_MIN))
            cv2.circle(frame_rgb, (a, b), r, (0, 255, 0), 2)
            pg.draw.circle(top_view, (0, 255, 0), (b, d1), h)

    if (fps := fps_medidor.update()) is not None:
        print(f'FPS:{fps}')

    frame_pg_front = pg.surfarray.make_surface(frame_rgb)

    # Display the frame on the pg window
    window.blit(frame_pg_front, (0, 0))
    window.blit(top_view, (0, window_height))

    pg.display.update()

    # Check if the 'Esc' key is pressed to exit the loop
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        break

    # clock.tick(40)

# Release resources
camera.release()
pg.quit()
