import cv2

# Inicialização da câmera
camera = cv2.VideoCapture(0)

while True:
    # Capturar frame da câmera
    ret, frame = camera.read()

    # Exibir o frame em uma janela
    cv2.imshow("Webcam", frame)

    # Nome do arquivo de saída
    output_file = "imagem_capturada.jpg"

    # Salvar a imagem em um arquivo JPEG
    cv2.imwrite(output_file, frame)


    # Verificar se a tecla 'Esc' foi pressionada para sair do loop
    if cv2.waitKey(1) == 27:
        break

# Liberar recursos
camera.release()
cv2.destroyAllWindows()
