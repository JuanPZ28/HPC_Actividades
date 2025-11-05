import imageio.v2 as iio #Carga de imagenes
import matplotlib.pyplot as plt #muestra de datos
import numpy as np #liberia de numeros
import time #mediciones de tiempo
import math
from multiprocessing import Process, shared_memory

IMAGE ="C:/Users/juand/OneDrive/Escritorio/SNEAKER-TECT/Imagenes/Pikachu.jpg"
WORKERS= 4

def worker(shm_name, shape, dtype, start, end):

  shm= shared_memory.SharedMemory(name=shm_name)
  resultado= np.ndarray(shape=shape, dtype=dtype, buffer=shm.buf)

  Gx_kernel = np.array([[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]], dtype=np.int32)
  Gy_kernel = np.array([[-1, -2, -1],
                  [ 0,  0,  0],
                  [ 1,  2,  1]], dtype=np.int32)
  # Evitar tocar los bordes globales

  if start == 0:
      start = 1
  if end >= shape[0]:
      end = shape[0] - 1

  filas_locales = end - start
  columnas = shape[1]
  out_local = np.zeros((filas_locales, columnas), dtype=np.float32)

  # Calcular Sobel con el out local
  for i in range(start, end):
      for j in range(1, columnas - 1):
        gx = 0
        gy = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
              gx += resultado[i + di, j + dj] * Gx_kernel[di + 1, dj + 1]
              gy += resultado[i + di, j + dj] * Gy_kernel[di + 1, dj + 1]
        out_local[i - start, j] = math.hypot(gx, gy)

  #Escribir resultado

  for ii in range(filas_locales):
    for jj in range(columnas):
      if out_local[ii, jj] >= 360:
          resultado[start + ii, jj] = 255 # blanco
      else:
          resultado[start + ii, jj] = 0   # negro    
  shm.close()

def image_to_grayscale(img):
  imagen_gris = np.zeros_like(img)#Pasa a 0 el arreglo
  for row in range(len(img)):
    for column in range(len(img[row])):
        pixel = img[row][column]
        gray_value = np.mean(pixel)#filtra valor promedio del RGB por cada pixel y lo guarda en un float
        imagen_gris[row][column] = [gray_value, gray_value, gray_value]
  return imagen_gris

def sobel(imagen_gris, n_procesos):

  imagen_gris= np.array(imagen_gris)#Pasarlo a una matriz de valores de 3 canales

  #convertir a un array de enteros con signo para evitar overflow en multiplicaciones
  if imagen_gris.dtype == np.uint8:
      img_int = imagen_gris.astype(np.int32)
  else:
      img_int = imagen_gris.astype(np.int32)

  if img_int.ndim == 3:
      img_int = img_int[..., 0]  # usar el primer canal (R=G=B en tu conversión)

  filas, columnas = img_int.shape  # funciona para grayscale 2D    
  altura= len(img_int)
  split= altura//n_procesos

  #Creacion de bloque de memoria compartida
  shm = shared_memory.SharedMemory(create=True, size=img_int.nbytes)
  shared_img= np.ndarray(shape=img_int.shape, dtype=img_int.dtype, buffer=shm.buf)
  np.copyto(shared_img, img_int)

  #Creacion de procesos
  procesos= []
  for i in range(n_procesos):
    start= i*split
    end= (i+1)*split if i < n_procesos-1 else altura
    p= Process(target=worker, args=(shm.name, img_int.shape, img_int.dtype, start, end))
    procesos.append(p)

  for p in procesos:
    p.start()

  for p in procesos:
    p.join()

  out = np.copy(shared_img)
  shm.close()
  shm.unlink()

  out_color = np.zeros((filas, columnas, 3), dtype=np.uint8)
  print("filas (alto):", filas, "columnas (ancho):", columnas)
  for ii in range(filas):
    for jj in range(columnas):
      if out[ii, jj] == 255:
        out_color[ii, jj] = [255, 255, 255]
      else:
        out_color[ii, jj] = [0, 0, 0]
  return out_color

def execution(img, method):
  imagen_gris= method(img)

  inicio=time.perf_counter()
  imagen_sobel = sobel(imagen_gris,WORKERS)
  fin=time.perf_counter()
  tiempo_ejecucion=fin-inicio

  print(f"Tiempo de ejecucion: {tiempo_ejecucion} segundos")
  return imagen_gris, imagen_sobel, tiempo_ejecucion
if __name__ == "__main__":
  img = iio.imread(IMAGE)

  # ADDED: ajustado unpacking para recibir la imagen sobel también
  imagen_gris, imagen_sobel, tiempo_ejecucion = execution(img, method=image_to_grayscale)


  fig, axes = plt.subplots(1, 3, figsize=(15, 5))
  plt.suptitle(f"ALGORITMO PARALELO- Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos", fontsize=16)
  axes[0].imshow(img)
  axes[0].set_title("Original")
  axes[1].imshow(imagen_gris)  # asegurarse dtype correcto para mostrar
  axes[1].set_title("Imagen en grises")
  axes[2].imshow(imagen_sobel)
  axes[2].set_title("Sobel")
  plt.show()