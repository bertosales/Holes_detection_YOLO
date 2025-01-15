import cv2
import os

pasta_imagens = "imagens_capturadas"
if not os.path.exists(pasta_imagens):
    os.makedirs(pasta_imagens)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Pressione 'Espaço' para capturar uma imagem e 'Esc' para sair.")

contador = 1  # Contador para nomear as imagens

while True:
    ret, frame = camera.read()

    if not ret:
        print("Erro: Não foi possível ler o frame da câmera.")
        break

    cv2.imshow("Webcam - Pressione Espaço para capturar", frame)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == 27:  # Aperte a tecla 'Esc' para sair
        print("Encerrando a captura.")
        break
    elif tecla == 32:  # Aperte a tecla 'Espaço' para capturar a imagem
        nome_imagem = f"imagem_{contador}.png"
        caminho_imagem = os.path.join(pasta_imagens, nome_imagem)
        if cv2.imwrite(caminho_imagem, frame):
            print(f"Imagem capturada e salva como: {caminho_imagem}")
            contador += 1
        else:
            print("Erro ao salvar a imagem.")

camera.release()
cv2.destroyAllWindows()
