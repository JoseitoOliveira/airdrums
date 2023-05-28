import traceback

import cv2
import pygame as pg
import pygame_widgets
from detection import detectar_esfera, process_image
from drum_element import DrumElement
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from utils import FPSMedidor

# Initialize pg mixer
pg.mixer.init()

# Camera initialization
camera = cv2.VideoCapture(2)

window_width = 800
window_height = 600

IS_TOP_VIEW = True
DISTANCIA_FOCAL = 26  # mm
TAMANHO_REAL = 50  # mm
D_MAX = 180
D_MIN = 60
H_MAX = 40
H_MIN = 20

# Coordinates and dimensions of the rectangle
drum_set = [
    DrumElement(
        'Snare',
        x=round(0.65 * window_height),
        y=round(0.4 * window_width),
        d=round(0.7 * window_height),
        ax1=round(0.07 * window_height),
        ax2=round(0.12 * window_width),
        angle=0,
        image='images/drum.png',
        sound='sounds/caixa.mp3'
    ),
    DrumElement(
        'Hi-hat',
        x=round(0.5 * window_height),
        y=round(0.15 * window_width),
        d=round(0.65 * window_height),
        ax1=round(0.09 * window_height),
        ax2=round(0.12 * window_width),
        angle=0,
        image='images/plate.png',
        sound='sounds/chimbal.mp3'
    ),
    DrumElement(
        'Ride-Cymbal',
        x=round(0.25 * window_height),
        y=round(0.9 * window_width),
        d=round(0.35 * window_height),
        ax1=round(0.15 * window_height),
        ax2=round(0.18 * window_width),
        angle=15,
        image='images/plate.png',
        sound='sounds/prato.mp3'
    )
]


# pg initialization
pg.init()
top_view = pg.Surface((window_width, window_width))
menu_lateral = pg.Surface((300, window_width))


def create_slider_with_output(surf, x, y, min=0, max=99, step=1):
    slider = Slider(surf, x + 30, y + 5, 250, 10, min=min, max=max, step=step)
    output = TextBox(surf, x, y, 20, 20, fontSize=15)
    output.disable()  # Act as label instead of textbox

    return slider, output


# Window dimensions
window = pg.display.set_mode((window_width + 300, window_width))

slider1, output1 = create_slider_with_output(window, window_width + 10, 60)
slider2, output2 = create_slider_with_output(window, window_width + 10, 90)
slider3, output3 = create_slider_with_output(window, window_width + 10, 120)
slider4, output4 = create_slider_with_output(window, window_width + 10, 150)
slider5, output5 = create_slider_with_output(window, window_width + 10, 180)


def togle_view():
    global IS_TOP_VIEW
    IS_TOP_VIEW = not IS_TOP_VIEW


btn_toglle_view = Button(
    # Mandatory Parameters
    window,  # Surface to place button on
    window_width + 10,  # X-coordinate of top left corner
    10,  # Y-coordinate of top left corner
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


fps_medidor = FPSMedidor()

while True:
    events = pg.event.get()
    for event in events:
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

    try:
        circles = detectar_esfera(frame_bgr)
    except Exception:
        traceback.print_exc()
        circles = []

    menu_lateral.fill((241, 243, 244))
    if IS_TOP_VIEW:
        top_view.fill((241, 243, 244))
    else:
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    for drum_ele in drum_set:
        drum_ele.interact_with_circles(circles)
        if IS_TOP_VIEW:
            drum_ele.draw_top_pygame(top_view)
        else:
            drum_ele.draw_front_opencv(frame_rgb)
        for c in circles:
            a, b, r = c[0], c[1], c[2]
            if IS_TOP_VIEW:
                d0 = (TAMANHO_REAL * DISTANCIA_FOCAL) / (2 * r)
                d1 = round((d0 + D_MIN) * (window_width / (D_MAX - D_MIN)))
                h = round(H_MAX - (a / window_height) * (H_MAX - H_MIN))
                pg.draw.circle(top_view, (0, 255, 0), (b, d1), h)
            else:
                cv2.circle(frame_rgb, (a, b), r, (0, 255, 0), 2)

    if (fps := fps_medidor.update()) is not None:
        print(f'FPS:{fps}')

    if IS_TOP_VIEW:
        window.blit(top_view, (0, 0))
    else:
        frame_pg_front = pg.surfarray.make_surface(frame_rgb)
        window.blit(frame_pg_front, (0, (window_width - window_height)//2))

    window.blit(menu_lateral, (window_width, 0))

    # Display the frame on the pg window

    output1.setText(slider1.getValue())
    output2.setText(slider2.getValue())
    output3.setText(slider3.getValue())
    output4.setText(slider4.getValue())
    output5.setText(slider5.getValue())

    pygame_widgets.update(events)
    pg.display.update()

    # Check if the 'Esc' key is pressed to exit the loop
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        break

# Release resources
camera.release()
pg.quit()
