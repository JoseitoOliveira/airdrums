import cv2

# Carrega a imagem
image = cv2.imread('image.jpg')

# Separa o canal azul
blue, green, red = cv2.split(image)
# Converte para uma imagem em escala de cinza
# Cria uma nova imagem utilizando apenas o canal azul
blue_image = cv2.merge((blue, blue, blue))
gray_image = cv2.cvtColor(blue_image, cv2.COLOR_BGR2GRAY)

# Exibe a imagem em escala de cinza
cv2.imshow("Imagem em Escala de Cinza", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()