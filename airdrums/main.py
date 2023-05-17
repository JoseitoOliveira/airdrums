"""
With PyGame
"""
import pygame
import cv2
import time

# Inicialização do Pygame
pygame.init()

# Definição das dimensões da janela
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))

# Inicialização da câmera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

# Variáveis para cálculo do FPS e do Delay
fps_start_time = time.time()
fps_frame_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Fechar a janela se o botão de fechar for pressionado
            camera.release()
            pygame.quit()
            quit()

    # Capturar tempo de início do processamento
    processing_start_time = time.time()

    # Capturar frame da câmera
    ret, frame = camera.read()

    # Rotacionar o frame em 90 graus no sentido anti-horário
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Converter a imagem do OpenCV para o formato do Pygame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pygame = pygame.surfarray.make_surface(frame_rgb)

    # Exibir o frame na janela do Pygame
    window.blit(frame_pygame, (0, 0))

    # Cálculo do FPS
    fps_frame_count += 1
    if (time.time() - fps_start_time) > 1:
        fps = fps_frame_count / (time.time() - fps_start_time)
        print("FPS:", round(fps, 2))
        fps_frame_count = 0
        fps_start_time = time.time()

    # Cálculo do Delay
    processing_time = time.time() - processing_start_time
    print("Delay:", round(processing_time, 4), "s")

    pygame.display.update()

    # Verificar se a tecla 'Esc' foi pressionada para sair do loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break

# Liberar recursos
camera.release()
pygame.quit()
