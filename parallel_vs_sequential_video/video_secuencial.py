from cv2 import VideoCapture
import cv2
import os
import shutil
import numpy as np
import shutil #manipulacion de archivos y carpetas de manera local
import time #mediciones de tiempo

#Creacion de archivos y sus rutas
folder_path_video ="C:/Users/juand/OneDrive/Escritorio/TAREAS_HPC/parallel_vs_sequential_video/video"
#Carpeta que guarda los frames a color del video
folder_path_frames_video_original="C:/Users/juand/OneDrive/Escritorio/TAREAS_HPC/parallel_vs_sequential_video/frames_video_original"
#Carpeta que guarda los frames a escala de grises del video
folder_path_frames_video_result= "C:/Users/juand/OneDrive/Escritorio/TAREAS_HPC/parallel_vs_sequential_video/frames_video_result"

#Video de resultado
video_result_fps = 30 # frames por segundo
#_--------------------------------------------------------
def image_to_grayscale(img):
  imagen_gris = np.zeros_like(img)#Pasa a 0 el arreglo
  for row in range(len(img)):
    for column in range(len(img[row])):
        pixel = img[row][column]
        gray_value = np.mean(pixel)#filtra valor promedio del RGB por cada pixel y lo guarda en un float
        imagen_gris[row][column] = [gray_value, gray_value, gray_value]
  return imagen_gris
#----------------------------------------------------------
#Eliminar carpetas si existen 
for folder in [folder_path_video, folder_path_frames_video_original, folder_path_frames_video_result, "sample_data"]:
    if os.path.exists(folder):
        shutil.rmtree(folder)  # elimina toda la carpeta y su contenido

#Crear carpetas nuevamente
os.makedirs(folder_path_video, exist_ok=True)
os.makedirs(folder_path_frames_video_original, exist_ok=True)
os.makedirs(folder_path_frames_video_result, exist_ok=True)

print("Ambiente limpio")

#Subir el video 

#ruta del video
ruta_video="C:/Users/juand/OneDrive/Escritorio/TAREAS_HPC/parallel_vs_sequential_video/video_original.mp4"
#cargar el video
video_color= cv2.VideoCapture(ruta_video)
#Obtener frames del input
fps= video_color.get(cv2.CAP_PROP_FPS)
#Cantidad de frames contados del input
total_frames=int(video_color.get(cv2.CAP_PROP_FRAME_COUNT))
duracion= total_frames / fps if fps > 0 else 0

print(f"FPS: {fps:.2f} | Frames totales: {total_frames} | Duración: {duracion:.2f} s")

#Obtener los frames y guardarlos en la carpeta

seconds_interval = 1/video_result_fps  # extraer un frame cada X segundos, cuanto durara cada frame del result
step = int(video_result_fps * seconds_interval)# Indica cada cuantos frames se deben saltar, cada cuanto quiero una imagen
#contadores
frame_idx=0
saved_count=0

while True:
    ret, frame = video_color.read()
    if not ret:
        break

    # Solo guardar frames en los intervalos deseados
    if frame_idx % step == 0:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Guardar como imagen
        output_path = os.path.join(folder_path_frames_video_original, f"frame_{saved_count:09d}.jpg")
        cv2.imwrite(output_path, cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))

        saved_count += 1

    frame_idx += 1

video_color.release()

print(f"Procesados: {frame_idx:,} frames")
print(f"Guardados:  {saved_count:,} frames (1 cada {seconds_interval}s)")

#AQUI INICIAN LOS WORKERS EN PARALELO
inicio=time.perf_counter()

#Cargar las imagenes
save_gray_count=0
for i in range(saved_count):
    # Formato del nombre de archivo con 9 ceros de relleno (000000000, 000000001, ...)
    filename = f"frame_{i:09d}.jpg"

    # Construir la ruta completa al archivo
    file_path = os.path.join(folder_path_frames_video_original, filename)

    # Verificar si el archivo existe antes de intentar leerlo
    if os.path.exists(file_path):
        # 6.1. Leer la imagen. OpenCV (cv2.imread) la lee por defecto en formato BGR.
        # Devuelve un array NumPy (alto, ancho, 3) con dtype uint8.
        bgr_image = cv2.imread(file_path)

        # 6.2. Convertir de BGR a RGB
        # El formato RGB es más estándar para visualización con librerías como matplotlib
        # y para muchos modelos de Machine Learning.
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        gray_image = image_to_grayscale(rgb_image)

        output_color= os.path.join(folder_path_frames_video_result, f"frame_{save_gray_count:09d}.jpg")
        cv2.imwrite(output_color, cv2.cvtColor(gray_image, cv2.COLOR_RGB2BGR))
        save_gray_count+=1

        print(f"imagen {i} leida:{filename} {rgb_image.shape}")

fin=time.perf_counter()
tiempo_ejecucion=fin-inicio
if tiempo_ejecucion > 100:
    print(f"\n Tiempo de ejecucion: {tiempo_ejecucion/60} minuto/s")
else:
    print(f"\n Tiempo de ejecucion: {tiempo_ejecucion} segundos")

# --- 1. Parámetros de Entrada y Salida ---
# Directorio donde están tus imágenes
folder_path = folder_path_frames_video_result

# Nombre del archivo de salida
video_name = 'video_result.mp4'

#Ruta
output_path = os.path.join(folder_path_video, video_name)

# Conteo total de frames
total_frames = saved_count

# Tasa de frames por segundo (FPS) del video final
fps = video_result_fps

# Primer frame para determinar las dimensiones (alto y ancho)
first_frame_name = f"frame_{0:09d}.jpg"
first_frame_path = os.path.join(folder_path, first_frame_name)

# Verificar si el primer frame existe y leerlo
if not os.path.exists(first_frame_path):
    print(f"Error: No se encontró el primer frame en {first_frame_path}")
    exit()

# Leer el primer frame para obtener las dimensiones
frame = cv2.imread(first_frame_path)
height, width, layers = frame.shape
frame_size = (width, height)

# --- 2. Configurar VideoWriter ---
# Codec (usando 'mp4v' para archivos MP4, ampliamente soportado)
# Asegúrate de que el codec sea compatible con tu entorno de Colab.
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Crear el objeto VideoWriter
video = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

print(f"Iniciando la creación del video '{video_name}' con resolución {width}x{height} y {fps} FPS...")

# --- 3. Iterar y Escribir Frames ---
for i in range(total_frames):
    # Generar el nombre de archivo con 9 ceros de relleno
    filename = f"frame_{i:09d}.jpg"
    file_path = os.path.join(folder_path, filename)

    # Cargar la imagen
    img = cv2.imread(file_path)

    if img is not None:
        # Escribir el frame en el video
        video.write(img)
    else:
        print(f"Advertencia: No se pudo cargar la imagen {filename}. Saltando.")

# --- 4. Liberar el Objeto VideoWriter ---
video.release()
print("\n¡Proceso terminado!")
print(f"El video se ha guardado como: {video_name}")
