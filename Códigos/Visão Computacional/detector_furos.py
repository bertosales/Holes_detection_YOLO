import cv2
import torch
from time import time

# Insira o caminho para o modelo treinado "best.pt"
model_path = 'C:\\Users\\TCC\\best.pt'

# Carregue o YOLOv5 (pasta compactada "yolov5.zip")
model = torch.hub.load('C:\\Users\\TCC\\yolov5', 'custom', path=model_path, source='local')

# Digite as posições dos furos (em milímetros)
posicao_furos = [ # Posição dos Furos do arquivo: peca_1.dxf
    {"furo": 1, "pos_x": 25.00, "pos_y": 37.00},
    {"furo": 2, "pos_x": 23.00, "pos_y": 13.00},
]
# Defina o limite de tolerância de posição para verificar furos próximos
tolerancia = 3.0  # Limite de tolerância para considerar furos como sendo na mesma posição (em mm)

# Digite o diâmetro do furo a ser verificado
diametro = 6
tolerancia_diam = 1  # Digite a tolerância do diâmetro em milímetros

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

# Escalas de conversão (pixels para milímetros)
resolucao_x = 640
resolucao_y = 480
largura_mm = 110
altura_mm = 85

escala_x = largura_mm / resolucao_x
escala_y = altura_mm / resolucao_y

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o quadro da câmera.")
        break

    start_time = time()

    results = model(frame)
    predictions = results.xyxy[0].cpu().numpy()

    tabuas_coords = []
    furos_coords = []

    for *box, conf, cls in predictions:
        x_min, y_min, x_max, y_max = map(int, box)
        label = int(cls)

        if label == 1:  # Classe 1: Tábua
            tabuas_coords.append((x_min, y_min, x_max, y_max))
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, "Tabua", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        elif label == 0:  # Classe 0: Furo
            furos_coords.append((x_min, y_min, x_max, y_max))
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.putText(frame, "Furo", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Cálculo das posições de cada furo em relação às tábuas
    for furo_coords in furos_coords:
        furo_x = furo_coords[0] + (furo_coords[2] - furo_coords[0]) // 2
        furo_y = furo_coords[1] + (furo_coords[3] - furo_coords[1]) // 2

        diametro_furo = max(furo_coords[2] - furo_coords[0], furo_coords[3] - furo_coords[1])
        diametro_furo_mm = (diametro_furo * escala_x)

        # Verificar se o raio do furo está dentro da tolerância
        if abs(diametro_furo_mm - diametro) > tolerancia_diam:
            status_diam = "incorreto"
        else:
            status_diam = "correto"

        min_distance = float('inf')
        nearest_tabua_coords = None
        furos_corretos = 0

        # Para cada tábua, calcular se o furo está dentro dela
        for tabua_coords in tabuas_coords:
            tabua_x_min, tabua_y_min, tabua_x_max, tabua_y_max = tabua_coords

            if tabua_x_min <= furo_x <= tabua_x_max and tabua_y_min <= furo_y <= tabua_y_max:
                # Calcular a posição do furo em relação à tábua
                pos_x = furo_x - tabua_x_min
                pos_y = furo_y - tabua_y_min

                # Converter a posição do furo de pixels para milímetros
                pos_x_mm = pos_x * escala_x
                pos_y_mm = pos_y * escala_y

                # Comparar com as posições fornecidas manualmente
                for furo_manual in posicao_furos:
                    furo_manual_x = furo_manual["pos_x"]
                    furo_manual_y = furo_manual["pos_y"]

                    furo_invertido_x = largura_mm - furo_manual_x
                    furo_invertido_y = altura_mm - furo_manual_y

                    # Calcular a distância entre o furo detectado e as posições
                    distancia_furo_normal = ((pos_x_mm - furo_manual_x) ** 2 + (pos_y_mm - furo_manual_y) ** 2) ** 0.5
                    distancia_furo_invertida = ((pos_x_mm - furo_invertido_x) ** 2 + (
                                pos_y_mm - furo_invertido_y) ** 2) ** 0.5

                    # Verificar se o furo está dentro da tolerância
                    if distancia_furo_normal < tolerancia or distancia_furo_invertida < tolerancia:
                        if status_diam == "correto":
                            status = "correto"
                            cv2.putText(frame, f"Furo {furo_manual['furo']} CORRETO", (furo_x + 20, furo_y - 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 2)
                            furos_corretos += 1
                        else:
                            status = "incorreto"
                            cv2.putText(frame, "Furo INCORRETO", (furo_x + 20, furo_y - 30), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (0, 50, 255), 2)
                    else:
                        status = "incorreto"
                        cv2.putText(frame, "Furo INCORRETO", (furo_x + 20, furo_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 50, 255), 2)

                # Exibir a posição do furo no vídeo
                cv2.putText(frame, f"Pos: ({pos_x_mm:.2f}mm, {pos_y_mm:.2f}mm)", (furo_x + 20, furo_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, f"Diametro: {diametro_furo_mm:.2f}mm)", (furo_x + 20, furo_y + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    end_time = time()

    cv2.imshow('Detector de Furos', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
