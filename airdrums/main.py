"""
With PyGame
"""
import pygame
import cv2
import traceback
from detection import detect_circles, filter_color
from drum_element import DrumElement

# Initialize pygame mixer
pygame.mixer.init()

# Coordinates and dimensions of the rectangle
drum_set = [
    DrumElement('Snare', x=400, y=150, w=100, h=150, sound='sounds/caixa.mp3'),
    DrumElement('Hi-hat', x=350, y=0, w=20, h=150, sound='sounds/chimbal.mp3')
]

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

    if len(bboxes) >= NUM_TRACKED_OBJS:
        gray = filter_color(frame_bgr, lower=[90, 50, 160], upper=[130, 255, 255])
        ok, boxes = multitracker.update(gray)
        # Verificar quais trackers falharam na detecção
        failed_trackers = []
        circles = []
        for i, box in enumerate(boxes):
            if box is None or any(v == 0 for v in box):
                failed_trackers.append(i)
            else:
                (x1, y1, d, d) = box
                r = d // 2
                a, b = x1 + r, y1 + r
                circles.append((round(a), round(b), round(r)))

        if len(failed_trackers):
            multitracker = cv2.legacy.MultiTracker_create()
            bboxes = []


    elif 0 < len(bboxes) < NUM_TRACKED_OBJS:
        # update tracker; detect circles; if new circle is detected add to tracker
        ...
    else:
        try:
            circles = detect_circles(frame_bgr=frame_bgr)
        except Exception:
            traceback.print_exc()
            circles = []
        gray = filter_color(frame_bgr, lower=[90, 50, 160], upper=[130, 255, 255])
        for pt in circles[:NUM_TRACKED_OBJS]:
            a, b, r = pt[0], pt[1], pt[2]
            x1, y1 = (a - r), (b - r)
            bbox = (x1, y1, 2 * r, 2 * r)
            bboxes.append(bbox)
            multitracker.add(tracker, gray, bbox)

    print(bboxes)

    for pt in circles:
        a, b, r = pt[0], pt[1], pt[2]

        [ele.interact(pt) for ele in drum_set]
        # Draw the circumference of the circle.
        cv2.circle(frame_rgb, (a, b), r, (0, 255, 0), 2)

    [ele.draw(frame_rgb) for ele in drum_set]

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
