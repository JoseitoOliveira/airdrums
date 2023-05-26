"""
With PyGame
"""
import pygame
import cv2
import traceback
from detection import detect_circles, filter_color, detectar_esfera_azul, process_image
from drum_element import DrumElement
from utils import FPSMedidor

# Initialize pygame mixer
pygame.mixer.init()

# Coordinates and dimensions of the rectangle
drum_set = [
    DrumElement('Snare', x=400, y=200, ax1=30, ax2=60, angle=0, sound='sounds/caixa.mp3'),
    DrumElement('Hi-hat', x=350, y=60, ax1=30, ax2=60, angle=-10, sound='sounds/chimbal.mp3'),
    DrumElement('Ride-Cymbal', x=200, y=450, ax1=45, ax2=90, angle=15, sound='sounds/prato.mp3')
]

# Pygame initialization
pygame.init()

# Window dimensions
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))

# Camera initialization
camera = cv2.VideoCapture(1)
# Set webcam frame size
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

    if len(bboxes) >= NUM_TRACKED_OBJS:
        ok, boxes = multitracker.update(process_image(frame_bgr))
        # Verificar quais trackers falharam na detecção
        if ok:
            circles = []
            for i, box in enumerate(boxes):
                (x1, y1, d1, d2) = box
                r = (d1 + d2) // 4
                a, b = x1 + r, y1 + r
                circles.append((round(a), round(b), round(r)))
        else:
            multitracker = cv2.legacy.MultiTracker_create()
            bboxes = []

    elif 0 < len(bboxes) < NUM_TRACKED_OBJS:
        # update tracker; detect circles; if new circle is detected add to tracker
        ...
    else:
        try:
            circles = detectar_esfera_azul(frame_bgr)
        except Exception:
            traceback.print_exc()
            circles = []
        gray = process_image(frame_bgr)
        for pt in circles[:NUM_TRACKED_OBJS]:
            a, b, r = pt[0], pt[1], pt[2]
            x1, y1 = (a - r), (b - r)
            bbox = (x1, y1, 2 * r, 2 * r)
            bboxes.append(bbox)
            multitracker.add(tracker, gray, bbox)

    # print(bboxes)

    for c in circles:
        a, b, r = c[0], c[1], c[2]

        [ele.interact(c) for ele in drum_set]
        # Draw the circumference of the circle.
        cv2.circle(frame_rgb, (a, b), r, (0, 255, 0), 2)
        
        for drum_element in drum_set:
            pt = drum_element.ponto_mais_proximo(c)
            cv2.circle(frame_rgb, pt, 2, (255, 0, 0), 2)
            cv2.line(frame_rgb, pt, drum_element.f1, (0, 0, 255), 1)
            cv2.line(frame_rgb, pt, drum_element.f2, (0, 0, 255), 1)

    [ele.draw(frame_rgb) for ele in drum_set]

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
