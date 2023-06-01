
import cv2
from collections import namedtuple


P = namedtuple('P', ['x', 'y', 'r'])


def process_image(frame_bgr):
    # Converter a imagem para o espaço de cores HSV
    imagem_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Definir os intervalos de cor para a esfera azul
    verde_min = (40, 100, 80)
    verde_max = (100, 255, 255)

    # Criar uma máscara binária
    mascara = cv2.inRange(imagem_hsv, verde_min, verde_max)

    # Realizar operação de abertura na máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)

    return mascara


def detect_drumstick_tip(image):

    mascara = process_image(image)

    # Encontrar os contornos dos objetos na máscara
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos com base no tamanho ou outras características relevantes
    circles = []
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 200:  # Exemplo: filtro de área mínima
            # Encontrar o círculo mínimo que envolve o contorno
            ((x, y), (w, h), alpha) = cv2.minAreaRect(contorno)
            raio = min(w, h) / 2
            circles.append(P(x, y, raio))

    return circles
