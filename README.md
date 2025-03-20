# Detector de diferencias usando OpenCV
En este proyecto se utiliza OpenCV y NumPy para detectar diferencias entre dos imágenes. Se basa en la técnica de deteccion de bordes Sobel y contornos para resaltar las diferencias entre dos imagenes similares. 

## Requisitos
Tener instaladas las siguientes biblotecas en python:

 - cv2
 
 - numpy
 
 - imutils

## Descripcion del codigo
 1. Carga de imagenes:
     Se leen dos imagenes.
    
 2. Redimensionamiento:
     Se ajustan las imagenes a un tamaño proporcional para mejor visualizacion en la pantalla.
    
 3. Conversión a escala de grises:
     Se convierten las imagenes a escalas de grises para facilitar el procesamiento.
    
 4. Aplicación del filtro sobel:
     Se aplican filtros de Sobel en los ejes X e Y para detectar bordes en ambas imágenes.
    
 5. Comparación de Diferencias:
     Se calcula la diferencia entre los bordes detectados en las dos imágenes.
    
 6. Binarización y Dilatación:
     Se aplica un umbral para binarizar la imagen de diferencias y luego se dilatan las áreas detectadas.
    
 7. Dibujar cuadros en las diferencias:
     Se encuentran los contornos de las diferencias y se dibujan rectángulos en ambas imágenes para resaltarlas.
    
 8. Mostrar los resultados:
     Se concatenan y muestran las imágenes con las diferencias resaltadas.
    
   
## Notas 
- Ambas imagenes deben tener el mismo tamaño para evitar errores en la comparación.
- En caso de que las imágenes sean distintas, el programa detectará la imagen completa como una sola diferencia.

