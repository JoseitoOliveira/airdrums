import cv2
import numpy as np

# Carregar a imagem
imagem = cv2.imread('imagem_capturada.jpg', 0)

# Aplicar suavização para reduzir o ruído
imagem_suavizada = cv2.GaussianBlur(imagem, (9, 9), 2, 2)

# Detectar os círculos usando o algoritmo de detecção de Hough
circulos = cv2.HoughCircles(
    imagem_suavizada, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0
)

# Se os círculos forem encontrados, desenhar os círculos encontrados
if circulos is not None:
    circulos = np.round(circulos[0, :]).astype("int")
    
    for (x, y, raio) in circulos:
        # Desenhar o círculo e o centro
        cv2.circle(imagem, (x, y), raio, (0, 255, 0), 4)
        cv2.circle(imagem, (x, y), 3, (0, 0, 255), -1)

# Exibir a imagem resultante
cv2.imshow("Detecção de Círculos", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
