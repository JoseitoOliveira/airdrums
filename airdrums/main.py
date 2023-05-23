"""
With PyGame
"""
import pygame
import cv2
import traceback
from detection import detect_cicles
from threading import Thread


def verifica_colisao(rect, circle):
    x, y, w, h = rect
    center_x, center_y, radius = circle

    # Verifica se o círculo colide com o retângulo
    if center_x + radius < x or center_x - radius > x + w or \
       center_y + radius < y or center_y - radius > y + h:
        return False
    else:
        return True


# Inicializar o mixer do pygame
pygame.mixer.init()

# Carregar os arquivos de som em canais separados
canal1 = pygame.mixer.Channel(0)
caixa = pygame.mixer.Sound('sounds/caixa.mp3')


def emitir_beep():
    t = Thread(target=canal1.play, args=(caixa,), daemon=True)
    t.start()


# Coordenadas e dimensões do retângulo
x_r = 400
y_r = 100
width_r = 100
height_r = 150

# Inicialização do Pygame
pygame.init()

# Definição das dimensões da janela
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))

# Inicialização da câmera
camera = cv2.VideoCapture(0)
# Define o tempo de abertura da webcam
camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

tracker = cv2.legacy.TrackerCSRT_create()
multitracker = cv2.legacy.MultiTracker_create()
bboxes = []

NUM_TRACKED_OBJS = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Fechar a janela se o botão de fechar for pressionado
            camera.release()
            pygame.quit()
            quit()

    # Capturar frame da câmera
    ret, frame_bgr = camera.read()

    # Rotacionar o frame em 90 graus no sentido anti-horário
    frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

    if len(bboxes) == NUM_TRACKED_OBJS:
        # only tracker bboxes
        ...
    elif 0 < len(bboxes) < NUM_TRACKED_OBJS:
        # update tracker; detect circles; if new circle is detected add to tracker
        ...
    else:
        try:
            cicles = detect_cicles(frame_bgr=frame_bgr)
        except Exception:
            traceback.print_exc()
        else:
            cicles = []
        
        for pt in cicles:
            a, b, r = pt[0], pt[1], pt[2]
            pt1 = [(a - r), (b - r)]
            pt2 = [(a + r), (b + r)]
            

            # Draw the circumference of the circle.
            cv2.circle(frame_rgb, (a, b), 20, (0, 255, 0), 2)


    # Converter a imagem do OpenCV para o formato do Pygame
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    for pt in cicles:
        a, b, r = pt[0], pt[1], pt[2]

        if verifica_colisao(
            (x_r, y_r, width_r, height_r), (a, b, 20)
        ):
            emitir_beep()

        # Draw the circumference of the circle.
        cv2.circle(frame_rgb, (a, b), 20, (0, 255, 0), 2)

    # Desenha o retângulo na imagem
    cv2.rectangle(frame_rgb, (x_r, y_r), (x_r + width_r, y_r + height_r), (0, 0, 255), 2)

    frame_pygame = pygame.surfarray.make_surface(frame_rgb)

    # Exibir o frame na janela do Pygame
    window.blit(frame_pygame, (0, 0))

    pygame.display.update()

    # Verificar se a tecla 'Esc' foi pressionada para sair do loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break

# Liberar recursos
camera.release()
pygame.quit()
