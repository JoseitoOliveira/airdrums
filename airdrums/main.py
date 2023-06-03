import time
import traceback

import cv2
import numpy as np
import pygame as pg
import pygame_widgets
from camera import screen_to_real
from detection import detect_drumstick_tip
from drums_elements import DrumElement, DrumstickTip
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from utils import FPSMedidor, find_closest_pairs

# Initialize pg mixer
pg.mixer.init()

# Camera initialization
camera = cv2.VideoCapture(3)

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
        d=round(rescale(1.20, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.09 * window_height),
        ax2=round(0.15 * window_width),
        angle=0,
        image='images/drum.png',
        sound='sounds/caixa.mp3'
    ),
    DrumElement(
        'Hi-hat',
        x=round(0.65 * window_height),
        y=round(0.15 * window_width),
        d=round(rescale(1.2, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.09 * window_height),
        ax2=round(0.15 * window_width),
        angle=0,
        image='images/plate.png',
        sound='sounds/chimbal.mp3'
    ),
    DrumElement(
        'Tom-1',
        x=round(0.3 * window_height),
        y=round(0.25 * window_width),
        d=round(rescale(1.05, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.1 * window_height),
        ax2=round(0.13 * window_width),
        angle=15,
        image='images/drum.png',
        sound='sounds/tom1.mp3'
    ),
    DrumElement(
        'Tom-2',
        x=round(0.3 * window_height),
        y=round(0.6 * window_width),
        d=round(rescale(1.05, D_MIN, D_MAX, 0, window_height)),
        ax1=round(0.12 * window_height),
        ax2=round(0.16 * window_width),
        angle=15,
        image='images/drum.png',
        sound='sounds/tom2.mp3'
    ),
    DrumElement(
        'Tom-3',
        x=round(0.9 * window_height),
        y=round(0.8 * window_width),
        d=round(rescale(1.15, D_MIN, D_MAX, 0, window_height)),
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
        d=round(rescale(1.15, D_MIN, D_MAX, 0, window_height)),
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
    30,  # X-coordinate of top left corner
    window_height // 2,  # Y-coordinate of top left corner
    30,  # Width
    30,  # Height

    # Optional Parameters
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    onClick=togle_view,  # Function to call when clicked on
    image=pg.image.load('images/girar-camera.png')
)

# # Set webcam frame size
camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)
camera.set(cv2.CAP_PROP_EXPOSURE, -7)
# camera.set(cv2.CAP_PROP_AUTO_WB, 1)


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

    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Aumenta o brilho ajustando o canal de brilho (valor V)
    brightness_offset = 50  # Ajuste esse valor para controlar o aumento do brilho
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + brightness_offset, 0, 255)

    # Converte a imagem de volta para o espaço de cores BGR
    frame_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Rotate the frame 90 degrees counterclockwise
    frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

    try:
        circles = detect_drumstick_tip(frame_bgr)
    except Exception:
        traceback.print_exc()
        circles = []

    # circles = [
    #     c for c in circles
    #     if screen_to_real(c.x, c.y, c.r, 50)[2] < 3
    # ]

    pairs, _drumstick_tips, _circles = find_closest_pairs(drumstick_tips, circles)

    for (dst, c) in pairs:
        dst.update_position(c.x, c.y, c.r)

    for dst in _drumstick_tips:
        if dst.num_erro_detection >= 3:
            drumstick_tips.remove(dst)
        else:
            dst.num_erro_detection += 1

    for c in _circles:
        drumstick_tips.append(DrumstickTip(c.x, c.y, c.r))

    if IS_TOP_VIEW:
        top_view.fill((241, 243, 244))
    else:
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_pg_front = pg.surfarray.make_surface(frame_rgb)
        front_view_pads = pg.surface.Surface((window_width, window_height), pg.SRCALPHA)

    for drum_ele in drum_set:
        drum_ele.interact_with_drumstick_tips(drumstick_tips)
        if IS_TOP_VIEW:
            drum_ele.draw_top(top_view)
        else:
            drum_ele.draw_front(front_view_pads)

    for tip in drumstick_tips:
        if IS_TOP_VIEW:
            d = rescale(tip.real_z, 0, 2, 0, window_width)
            pg.draw.circle(top_view, (0, 255, 0), (tip.y, d), 20)
        else:
            pg.draw.circle(frame_pg_front, (0, 255, 0), (tip.y, tip.x), tip.r)

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
