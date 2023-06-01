import time
import traceback

import cv2
import pygame as pg
import pygame_widgets
from detection import detect_drumstick_tip
from drum_element import DrumElement, DrumstickTip
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from utils import FPSMedidor, find_closest_pairs

# Initialize pg mixer
pg.mixer.init()

# Camera initialization
camera = cv2.VideoCapture(2)

window_width = 800
window_height = 600

IS_TOP_VIEW = True
D_MAX = 1.4
D_MIN = 0.8


def rescale(x, x0, x1, y0, y1):
    return ((x - x0) * (y1 - y0) / (x1 - x0)) + y0


# Coordinates and dimensions of the rectangle
drum_set = [
    DrumElement(
        'Snare',
        x=round(0.85 * window_height),
        y=round(0.4 * window_width),
        d=round(rescale(1.45, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.07 * window_height),
        ax2=round(0.12 * window_width),
        angle=0,
        image='images/drum.png',
        sound='sounds/caixa.mp3'
    ),
    DrumElement(
        'Hi-hat',
        x=round(0.75 * window_height),
        y=round(0.15 * window_width),
        d=round(rescale(1.5, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.09 * window_height),
        ax2=round(0.12 * window_width),
        angle=0,
        image='images/plate.png',
        sound='sounds/chimbal.mp3'
    ),
    DrumElement(
        'Tom-1',
        x=round(0.5 * window_height),
        y=round(0.3 * window_width),
        d=round(rescale(1.25, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.09 * window_height),
        ax2=round(0.1 * window_width),
        angle=15,
        image='images/drum.png',
        sound='sounds/tom1.mp3'
    ),
    DrumElement(
        'Tom-2',
        x=round(0.5 * window_height),
        y=round(0.55 * window_width),
        d=round(rescale(1.25, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.10 * window_height),
        ax2=round(0.13 * window_width),
        angle=15,
        image='images/drum.png',
        sound='sounds/tom2.mp3'
    ),
    DrumElement(
        'Tom-3',
        x=round(0.9 * window_height),
        y=round(0.8 * window_width),
        d=round(rescale(1.35, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.09 * window_height),
        ax2=round(0.13 * window_width),
        angle=15,
        image='images/drum.png',
        sound='sounds/tom3.mp3'
    ),
    DrumElement(
        'Ride-Cymbal',
        x=round(0.25 * window_height),
        y=round(1 * window_width),
        d=round(rescale(1.35, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.09 * window_height),
        ax2=round(0.18 * window_width),
        angle=15,
        image='images/plate.png',
        sound='sounds/prato.mp3'
    )
]


# pg initialization
pg.init()
clock = pg.time.Clock()
top_view = pg.Surface((window_width, window_width))


def create_slider_with_output(surf, x, y, min=0, max=99, step=1):
    slider = Slider(surf, x + 30, y + 5, 250, 10, min=min, max=max, step=step)
    output = TextBox(surf, x, y, 20, 20, fontSize=15)
    output.disable()  # Act as label instead of textbox

    return slider, output


# Window dimensions
window = pg.display.set_mode((window_width, window_width))


def togle_view():
    global IS_TOP_VIEW
    IS_TOP_VIEW = not IS_TOP_VIEW


btn_toglle_view = Button(
    # Mandatory Parameters
    window,  # Surface to place button on
    window_width - 60,  # X-coordinate of top left corner
    30,  # Y-coordinate of top left corner
    30,  # Width
    30,  # Height

    # Optional Parameters
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    onClick=togle_view,  # Function to call when clicked on
    image=pg.image.load('images/girar-camera.png')
)

# # Set webcam frame size
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)


fps_medidor = FPSMedidor()
drumstick_tips: list[DrumstickTip] = []

t1 = time.perf_counter()
while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            # Close the window if the close button is pressed
            camera.release()
            pg.quit()
            quit()

    # Capture frame from the camera
    td = time.perf_counter() - t1
    ret, frame_bgr = camera.read()
    t1 = time.perf_counter()

    if not ret:
        break

    # Rotate the frame 90 degrees counterclockwise
    frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

    try:
        circles = detect_drumstick_tip(frame_bgr)
    except Exception:
        traceback.print_exc()
        circles = []

    pairs, _drumstick_tips, _circles = find_closest_pairs(drumstick_tips, circles)

    for (dst, c) in pairs:
        dst.update_position(c.x, c.y, c.r)

    for dst in _drumstick_tips:
        ...

    for c in _circles:
        drumstick_tips.append(DrumstickTip(c.x, c.y, c.r))

    if IS_TOP_VIEW:
        top_view.fill((241, 243, 244))
    else:
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_pg_front = pg.surfarray.make_surface(frame_rgb)
        front_view_pads = pg.surface.Surface((window_width, window_height), pg.SRCALPHA)

    circles_3d: list[tuple[float, float, float, float]] = []
    for a, b, r in circles:
        d_real = (TAMANHO_REAL * DISTANCIA_FOCAL) / (2 * r)
        d_screen = rescale(d_real, 0, 2, 0, window_width)
        circles_3d.append((a, b, d_screen, r))

    for drum_ele in drum_set:
        drum_ele.interact_with_circles(circles_3d)
        if IS_TOP_VIEW:
            drum_ele.draw_top(top_view)
        else:
            drum_ele.draw_front(front_view_pads)

    for a, b, d, r in circles_3d:
        # print(f'x={2*0.25*r/0.05}')
        if IS_TOP_VIEW:
            h = H_MAX - (a / window_height) * (H_MAX - H_MIN)
            pg.draw.circle(top_view, (0, 255, 0), (b, d), h)
        else:
            pg.draw.circle(frame_pg_front, (0, 255, 0), (b, a), r)

    if (fps := fps_medidor.update()) is not None:
        print(f'FPS:{fps:.2f} PFPS:{1/td:.2f}')

    if IS_TOP_VIEW:
        window.blit(top_view, (0, 0))
    else:
        window.blit(frame_pg_front, (0, (window_width - window_height) // 2))
        window.blit(front_view_pads, (0, (window_width - window_height) // 2))

    pygame_widgets.update(events)
    pg.display.update()

    # Check if the 'Esc' key is pressed to exit the loop
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        break

    # clock.tick(30)

# Release resources
camera.release()
pg.quit()
