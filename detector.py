import cv2
import numpy as np
import matplotlib.pyplot as plt

def encontrar_diferencias(imagen1_path, imagen2_path):
    """
    Encuentra diferencias entre dos imágenes y las muestra circuladas.
    
    Args:
        imagen1_path: Ruta a la primera imagen
        imagen2_path: Ruta a la segunda imagen
    """
    # Cargar las imágenes
    imagen1 = cv2.imread(imagen1_path)
    imagen2 = cv2.imread(imagen2_path)
    
    # Verificar que se cargaron correctamente
    if imagen1 is None or imagen2 is None:
        print(f"Error: No se pudieron cargar las imágenes. Verifica las rutas:")
        print(f"Imagen 1: {imagen1_path}")
        print(f"Imagen 2: {imagen2_path}")
        return
    
    # Asegurar que las imágenes tengan el mismo tamaño
    if imagen1.shape != imagen2.shape:
        print("Las imágenes tienen diferentes dimensiones. Redimensionando...")
        imagen2 = cv2.resize(imagen2, (imagen1.shape[1], imagen1.shape[0]))
    
    # Convertir a escala de grises
    imagen1_gray = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
    imagen2_gray = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)
    
    # Aplicar filtro Gaussiano para suavizar imágenes
    imagen1_blur = cv2.GaussianBlur(imagen1_gray, (5, 5), 0)
    imagen2_blur = cv2.GaussianBlur(imagen2_gray, (5, 5), 0)
    
    # Calcular la diferencia absoluta entre las imágenes filtradas
    diferencia = cv2.absdiff(imagen1_blur, imagen2_blur)
    
    # Aplicar umbral para resaltar diferencias
    _, umbral = cv2.threshold(diferencia, 30, 255, cv2.THRESH_BINARY)
    
    # Limpiar ruido con operaciones morfológicas
    kernel = np.ones((5, 5), np.uint8)
    umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel)
    umbral = cv2.dilate(umbral, kernel, iterations=1)
    
    # Encontrar contornos de las diferencias
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos pequeños (probablemente ruido)
    contornos_filtrados = [c for c in contornos if cv2.contourArea(c) > 50]
    
    # Crear una copia de la imagen 2 para marcar las diferencias
    imagen_diferencias = imagen2.copy()
    
    # Dibujar círculos alrededor de las diferencias
    for contorno in contornos_filtrados:
        # Obtener el centro y radio del círculo
        (x, y), radio = cv2.minEnclosingCircle(contorno)
        centro = (int(x), int(y))
        radio = int(radio) + 10  # Hacer el círculo un poco más grande
        
        # Dibujar el círculo
        cv2.circle(imagen_diferencias, centro, radio, (0, 0, 255), 2)
    
    # Convertir las imágenes para mostrar con matplotlib (BGR a RGB)
    imagen1_rgb = cv2.cvtColor(imagen1, cv2.COLOR_BGR2RGB)
    imagen2_rgb = cv2.cvtColor(imagen2, cv2.COLOR_BGR2RGB)
    imagen_diferencias_rgb = cv2.cvtColor(imagen_diferencias, cv2.COLOR_BGR2RGB)
    
    # Crear ventana de visualización
    plt.figure(figsize=(15, 5))
    
    # Mostrar imagen 1
    plt.subplot(1, 3, 1)
    plt.imshow(imagen1_rgb)
    plt.title("Imagen 1")
    plt.axis("off")
    
    # Mostrar imagen 2
    plt.subplot(1, 3, 2)
    plt.imshow(imagen2_rgb)
    plt.title("Imagen 2")
    plt.axis("off")
    
    # Mostrar diferencias
    plt.subplot(1, 3, 3)
    plt.imshow(imagen_diferencias_rgb)
    plt.title(f"Diferencias Encontradas: {len(contornos_filtrados)}")
    plt.axis("off")
    
    # Ajustar espaciado y mostrar
    plt.tight_layout()
    plt.show()
    
    print(f"Se encontraron {len(contornos_filtrados)} diferencias entre las imágenes.")
    
    return contornos_filtrados

# Ejemplo de uso:
if __name__ == "__main__":
    # AQUÍ PUEDES CAMBIAR LAS RUTAS DE LAS IMÁGENES
    imagen1_path = "casita1.JPG"  # Cambia esto a la ruta de tu primera imagen
    imagen2_path = "casita2.JPG"  # Cambia esto a la ruta de tu segunda imagen
    
    # Ejecutar la función
    encontrar_diferencias(imagen1_path, imagen2_path)