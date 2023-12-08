import cv2
import numpy as np

# Ruta del video
video_path = 'tirada_2.mp4'

# Abre el video
cap = cv2.VideoCapture(video_path)

# Verifica si el video se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

# Configuración para detección de dados quietos
umbral_distancia_centroides = 9  # Ajusta este umbral según sea necesario
num_frames_estables = 30  # Número de frames estables para considerar que los dados están quietos

# Configuración para detección de números
umbral_binario_dados = 75
umbral_binario_numeros = 200
min_area_numero = 10  # Ajusta este valor según sea necesario

# Variables para seguimiento de centroides
centroids_anteriores = None
contador_frames_estables = 0

# Bucle para procesar cada frame
while True:
    # Lee el siguiente frame
    ret, frame = cap.read()

    # Sal del bucle si no hay más frames
    if not ret:
        break

    # Redimensiona el frame a la mitad
    resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # Extrae el canal rojo del frame redimensionado
    red_channel = resized_frame[:, :, 2]

    # Binariza la imagen usando un umbral (ajusta el valor del umbral según sea necesario)
    _, binary_frame_dados = cv2.threshold(red_channel, umbral_binario_dados, 255, cv2.THRESH_BINARY)

    # Encuentra los componentes conectados de los dados
    num_labels_dados, labels_dados, stats_dados, centroids_dados = cv2.connectedComponentsWithStats(binary_frame_dados, connectivity=8)

    # Filtra las componentes de dados por área y relación de aspecto
    dados_filtrados = []
    for label in range(1, num_labels_dados):
        area_dados = stats_dados[label, cv2.CC_STAT_AREA]

        # Ajusta estos valores según sea necesario para tu aplicación
        min_area_dados = 100
        max_area_dados = 10000
        aspect_ratio_threshold_dados = 1.2

        if min_area_dados <= area_dados <= max_area_dados:
            x_dados, y_dados, w_dados, h_dados = stats_dados[label, cv2.CC_STAT_LEFT], stats_dados[label, cv2.CC_STAT_TOP], stats_dados[label, cv2.CC_STAT_WIDTH], stats_dados[label, cv2.CC_STAT_HEIGHT]
            aspect_ratio_dados = float(w_dados) / h_dados

            if 1 / aspect_ratio_threshold_dados <= aspect_ratio_dados <= aspect_ratio_threshold_dados:
                dados_filtrados.append((x_dados, y_dados, x_dados + w_dados, y_dados + h_dados))  # Almacena las coordenadas de las bounding boxes

    # Mide la distancia entre centroides de frames consecutivos para todos los centroides
    if centroids_anteriores is not None:
        # Comprueba si los dados están "quietos"
        if np.linalg.norm(centroids_anteriores[0] - centroids_dados[0]) < umbral_distancia_centroides:
            contador_frames_estables += 1
        else:
            contador_frames_estables = 0

        # Si se han mantenido "quietos" durante un número suficiente de frames y hay 5 dados detectados, se procede
        if contador_frames_estables >= num_frames_estables and len(dados_filtrados) == 5:
            for bbox_dados in dados_filtrados:
                x_dados, y_dados, x_max_dados, y_max_dados = bbox_dados

                # Recorta la región de interés (ROI) para cada dado
                roi_dados = red_channel[y_dados:y_max_dados, x_dados:x_max_dados]

                # Binariza la ROI para detectar números
                _, binary_roi_numeros = cv2.threshold(roi_dados, umbral_binario_numeros, 255, cv2.THRESH_BINARY)

                # Encuentra componentes conectadas en la ROI binarizada
                num_labels_roi_numeros, _, stats_roi_numeros, _ = cv2.connectedComponentsWithStats(binary_roi_numeros, connectivity=8)

                # Filtra las componentes por área
                numeros_filtrados = [stats_roi_numeros[label, cv2.CC_STAT_AREA] for label in range(1, num_labels_roi_numeros) if stats_roi_numeros[label, cv2.CC_STAT_AREA] > min_area_numero]

                # Imprime la cantidad de números detectados en cada dado
                cantidad_numeros = len(numeros_filtrados)

                # Dibuja el rectángulo azul sobre el frame original
                cv2.rectangle(resized_frame, (x_dados, y_dados), (x_max_dados, y_max_dados), (255, 0, 0), 2)

                # Dibuja el número sobre el frame original
                cv2.putText(resized_frame, str(cantidad_numeros), (x_dados, y_dados-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    # Guarda los centroides para la próxima iteración
    centroids_anteriores = centroids_dados.copy()

    # Muestra el frame original con rectángulos dibujados
    cv2.imshow('Original Frame', resized_frame)

    # Espera 30 milisegundos y verifica si se presiona la tecla 'q' para salir
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Libera la captura de video y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
