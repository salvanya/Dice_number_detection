import cv2
import numpy as np

# Abrir el video -----------------------------------------------------------------------------------------------

# Ruta del video
video_path = 'tirada_1.mp4'
output_path = 'resultado_tirada_1.mp4'

# Abre el video
cap = cv2.VideoCapture(video_path)

# Verifica si el video se abrió correctamente
if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

# Parámetros ----------------------------------------------------------------------------------------------------

# Configuración para detección de dados quietos --------------------------------

# Umbral para considerar quietos a los centroides
umbral_distancia_centroides = 9
# Número de frames estables para considerar que los dados están quietos
num_frames_estables = 30  

# Configuración para detección dedados y números --------------------------------

# Definir umbrales de áreas y relación de aspecto para los dados
min_area_dados = 100
max_area_dados = 10000
aspect_ratio_threshold_dados = 1.2

# Umbral para la binarización para detectar dados
umbral_binario_dados = 75

# Umbral para la binarización para detectar los puntos de las caras
umbral_binario_numeros = 195

# Área mínima para considerar una componente conexa un punto de la cara
min_area_punto = 10

# Número de frames consecutivos para considerar estable el número de un dado
num_frames_estable_numero = 10  

# Variables para seguimiento de centroides y números ---------------------------------------------------------------------------
centroids_anteriores = None
contador_frames_estables = 0
# Crear diccionarios para determinar números estables 
numeros_estables = {i: {'numero': 0, 'contador_frames': 0, 'mostrar': False, 'condicion_activada': False} for i in range(5)}

# Configuración para el video de salida ----------------------------------------------------------------------------------------
output_size = (int(cap.get(3)*0.5), int(cap.get(4)*0.5))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, 30.0, output_size)


# Bucle para procesar cada frame -----------------------------------------------------------------------------------------------
while True:
    # Leer el siguiente frame
    ret, frame = cap.read()

    # Salir del bucle si no hay más frames
    if not ret:
        break

    # Redimensionar el frame a la mitad
    resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # Extraer el canal rojo del frame redimensionado
    red_channel = resized_frame[:, :, 2]

    # Binarizar la imagen usando un umbral
    _, binary_frame_dados = cv2.threshold(red_channel, umbral_binario_dados, 255, cv2.THRESH_BINARY)

    # Encontrar los componentes conectados de los dados
    num_labels_dados, labels_dados, stats_dados, centroids_dados = cv2.connectedComponentsWithStats(binary_frame_dados, connectivity=8)

    # Filtrar las componentes de dados por área y relación de aspecto
    dados_filtrados = []
    
    for label in range(1, num_labels_dados):
        
        area_dados = stats_dados[label, cv2.CC_STAT_AREA]

        if min_area_dados <= area_dados <= max_area_dados:
            x_dados, y_dados, w_dados, h_dados = stats_dados[label, cv2.CC_STAT_LEFT], stats_dados[label, cv2.CC_STAT_TOP], stats_dados[label, cv2.CC_STAT_WIDTH], stats_dados[label, cv2.CC_STAT_HEIGHT]
            aspect_ratio_dados = float(w_dados) / h_dados

            if 1 / aspect_ratio_threshold_dados <= aspect_ratio_dados <= aspect_ratio_threshold_dados:
                # Almacenar las coordenadas de las bounding boxes
                dados_filtrados.append((x_dados, y_dados, x_dados + w_dados, y_dados + h_dados))  

    # Medir la distancia entre centroides de frames consecutivos para todos los centroides
    if centroids_anteriores is not None:
        # Coomprobar si los dados están "quietos"
        if np.linalg.norm(centroids_anteriores[0] - centroids_dados[0]) < umbral_distancia_centroides:
            contador_frames_estables += 1
        else:
            contador_frames_estables = 0

        # Si se han mantenido "quietos" durante un número suficiente de frames y hay 5 dados detectados, se procede:
        if contador_frames_estables >= num_frames_estables and len(dados_filtrados) == 5:

            # Flag para la activación inicial
            if not any(numero_estable['condicion_activada'] for numero_estable in numeros_estables.values()):
                for numero_estable in numeros_estables.values():
                    numero_estable['condicion_activada'] = True

            for bbox_dados in dados_filtrados:
                x_dados, y_dados, x_max_dados, y_max_dados = bbox_dados

                # Recorta la región de interés (ROI) para cada dado
                roi_dados = red_channel[y_dados:y_max_dados, x_dados:x_max_dados]

                # Binarizar la ROI para detectar números
                _, binary_roi_numeros = cv2.threshold(roi_dados, umbral_binario_numeros, 255, cv2.THRESH_BINARY)

                # Encontrar componentes conectadas en la ROI binarizada
                num_labels_roi_numeros, _, stats_roi_numeros, _ = cv2.connectedComponentsWithStats(binary_roi_numeros, connectivity=8)

                # Filtrar las componentes por área
                componentes_filtradas_puntos = [stats_roi_numeros[label, cv2.CC_STAT_AREA] for label in range(1, num_labels_roi_numeros) if stats_roi_numeros[label, cv2.CC_STAT_AREA] > min_area_punto]

                # Obtener la cantidad de puntos detectados en cada dado
                cantidad_numeros = len(componentes_filtradas_puntos)

                # Actualizar el número estable detectado para el dado actual
                numeros_estables[dados_filtrados.index(bbox_dados)]['numero'] = cantidad_numeros
                numeros_estables[dados_filtrados.index(bbox_dados)]['contador_frames'] += 1
                numeros_estables[dados_filtrados.index(bbox_dados)]['mostrar'] = True

                # Verificar si el número ha sido estable durante el número requerido de frames consecutivos
                if numeros_estables[dados_filtrados.index(bbox_dados)]['contador_frames'] >= num_frames_estable_numero:
                    
                    # Dibujar el rectángulo azul sobre el frame original
                    cv2.rectangle(resized_frame, (x_dados, y_dados), (x_max_dados, y_max_dados), (255, 0, 0), 2)

                    # Dibujar el número sobre el frame original
                    cv2.putText(resized_frame, str(cantidad_numeros), (x_dados, y_dados - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                                cv2.LINE_AA)
        else:
            # Si no se cumplen las condiciones, oculta los números de los dados
            for numero_estable in numeros_estables.values():
                numero_estable['mostrar'] = False
                # Restablecer la segunda flag si se rompe la condición
                if numero_estable['condicion_activada']:
                    numero_estable['contador_frames'] = 0
                    numero_estable['condicion_activada'] = False

    # Guardar los centroides para la próxima iteración
    centroids_anteriores = centroids_dados.copy()

    # Mostrar el frame original con rectángulos dibujados
    cv2.imshow('Original Frame', resized_frame)

    # Guardar el frame en el video de salida
    out.write(resized_frame)

    # Esperar 30 milisegundos y verifica si se presiona la tecla 'q' para salir
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar la captura de video, cerrar el video de salida y las ventanas
cap.release()
out.release()
cv2.destroyAllWindows()