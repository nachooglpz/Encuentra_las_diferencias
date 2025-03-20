# Detector de diferencias usando OpenCV
En este proyecto se utiliza OpenCV y NumPy para detectar diferencias entre dos imágenes. Se basa en la técnica de deteccion de bordes Sobel y contornos para resaltar las diferencias entre dos imagenes similares. 

## Requisitos
Tener instaladas las siguientes biblotecas en python:
 cv2
 numpy
 imutils

## Descripcion del codigo
 Carga de imagenes:
     Se leen dos imagenes (adtime1.jpg y adtime2.jpg).
 Redimensionamiento:
     Se ajustan las imagenes a un tamaño proporcional para mejor visualizacion en la pantalla para casos de diferencias de resolución.
 Conversión a escala de grises:
     Se convierten las imagenes a escalas de grises para facilitar el proceso.
 Aplicación del filtro sobel:
     Se aplican filtros de Sobel en los ejes X e Y para detectar bordes en ambas imágenes.
 Comparación de Diferencias:
     Se calcula la diferencia entre los bordes detectados en las dos imágenes.
 Binarización y Dilatación:
     Se aplica un umbreal para binarizar la imagen de diferencias y luego se dilatan las áreas detectadas.
 Dibujar cuadros en las diferencias:
     Se encuentran los contornos de las diferencias y se dibujan rectángulos en ambas imágenes para resaltarlas.
 Mostrar los resultados:
     Se concatenan y muestran las imágenes con las diferencias resaltadas.
   
