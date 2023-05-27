
import cv2
import numpy as np



def process_image(frame_bgr):
    # Converter a imagem para o espaço de cores HSV
    imagem_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Definir os intervalos de cor para a esfera azul
    azul_min = (90, 120, 70)
    azul_max = (130, 255, 255)

    # Criar uma máscara binária
    mascara = cv2.inRange(imagem_hsv, azul_min, azul_max)

    # Realizar operação de abertura na máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)

    return mascara


def detectar_esfera_azul(image):

    mascara = process_image(image)

    # Encontrar os contornos dos objetos na máscara
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos com base no tamanho ou outras características relevantes
    circles = []
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 200:  # Exemplo: filtro de área mínima
            # Encontrar o círculo mínimo que envolve o contorno
            (x, y), raio = cv2.minEnclosingCircle(contorno)
            # # Distance Transform
            # mask = np.zeros_like(bin, dtype=np.uint8)
            # cv2.drawContours(mask, contorno, 0, 255, cv2.FILLED)
            # dt = cv2.distanceTransform(mask, cv2.DIST_L2, 5, cv2.DIST_LABEL_PIXEL)

            # # Find max value
            # minVal, max_val, _, max_loc = cv2.minMaxLoc(dt)
            # raio = minVal / 2
            circles.append((round(x), round(y), round(raio)))

    return circles
