import imageio.v2 as iio #Carga de imagenes
import matplotlib.pyplot as plt #muestra de datos 
import numpy as np #liberia de numeros 
import time #mediciones de tiempo
import math
IMAGE ="C:/Users/juand/OneDrive/Escritorio/SNEAKER-TECT/Imagenes/Pikachu.jpg"
def image_to_grayscale(img):
  imagen_gris = np.zeros_like(img)#Pasa a 0 el arreglo
  for row in range(len(img)):
    for column in range(len(img[row])):
        pixel = img[row][column]
        gray_value = np.mean(pixel)#filtra valor promedio del RGB por cada pixel y lo guarda en un float
        imagen_gris[row][column] = [gray_value, gray_value, gray_value]
  return imagen_gris

def sobel(imagen_gris):
  imagen_gris= np.array(imagen_gris)#Pasarlo a una matriz 

  #convertir a un array de enteros con signo para evitar overflow en multiplicaciones
  if imagen_gris.dtype == np.uint8:
      img_int = imagen_gris.astype(np.int32)   # o np.int16
  else:
      img_int = imagen_gris.astype(np.int32)

  if img_int.ndim == 3:
      img_int = img_int[..., 0]  # usar el primer canal (R=G=B)

  Gx_kernel = np.array([[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]], dtype=np.int32)
  Gy_kernel = np.array([[-1, -2, -1],
                  [ 0,  0,  0],
                  [ 1,  2,  1]], dtype=np.int32)

  filas, columnas = img_int.shape  # funciona para grayscale 2D
  print("filas (alto):", filas, "columnas (ancho):", columnas)

  out = np.zeros((filas, columnas), dtype=np.float32)  # magnitud en float
  for i in range(1, filas-1):
    for j in range(1,columnas-1):
      gx=0
      gy=0
      for di in range(-1,2):#-1,0,1
        for dj in range(-1,2):#-1,0,1
          gx += img_int[i+di, j+dj] * Gx_kernel[di+1, dj+1] #Ya que estas matrices inician en 0
          gy += img_int[i+di, j+dj] * Gy_kernel[di+1, dj+1]
      out[i,j]=math.hypot(gx, gy)#Calculo con precision numerica para imagenes

  out_color = np.zeros((filas, columnas, 3), dtype=np.uint8)
  for ii in range(filas):
    for jj in range(columnas):
      if out[ii, jj] >= 360:
        out_color[ii, jj] = [255, 255, 255]
      else:
        out_color[ii, jj] = [0, 0, 0]

  return out_color

def execution(img, method):
  imagen_gris= method(img)

  inicio=time.perf_counter()
  imagen_sobel = sobel(imagen_gris)

  fin=time.perf_counter()
  tiempo_ejecucion=fin-inicio
  print(f"Tiempo de ejecucion: {tiempo_ejecucion} segundos")
  return imagen_gris, imagen_sobel, tiempo_ejecucion
if __name__ == "__main__":
  img = iio.imread(IMAGE)

  imagen_gris, imagen_sobel, tiempo_ejecucion = execution(img, method=image_to_grayscale)


  fig, axes = plt.subplots(1, 3, figsize=(15, 5))
  plt.suptitle(f"ALGORITMO SECUENCIAL- Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos", fontsize=16) 
  axes[0].imshow(img)
  axes[0].set_title("Original")
  axes[1].imshow(imagen_gris)  # asegurarse dtype correcto para mostrar
  axes[1].set_title("Imagen en grises")
  axes[2].imshow(imagen_sobel) 
  axes[2].set_title("Sobel")

  plt.show()
