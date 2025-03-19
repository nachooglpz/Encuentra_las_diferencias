import cv2
import numpy as np
import argparse
import os

def detectar_cambios_ilustraciones(imagen1_path, imagen2_path, sensibilidad=15, area_minima=50, mostrar=True, guardar=False):
    """
    Detecta cambios entre dos ilustraciones o imágenes con estilos gráficos.
    Optimizado para detectar cambios sutiles en colores y formas.
    
    Args:
        imagen1_path: Ruta a la primera imagen (original)
        imagen2_path: Ruta a la segunda imagen (con cambios)
        sensibilidad: Nivel de sensibilidad (más bajo = más sensible)
        area_minima: Área mínima de los cambios a considerar (en píxeles)
        mostrar: Si es True, muestra las imágenes
        guardar: Si es True, guarda la imagen con los cambios detectados
        
    Returns:
        imagen_resultado: Imagen con los cambios marcados
        cambios_detectados: Número de cambios detectados
    """
    # Cargar imágenes
    imagen1 = cv2.imread(imagen1_path)
    imagen2 = cv2.imread(imagen2_path)
    
    # Verificar que las imágenes se cargaron correctamente
    if imagen1 is None or imagen2 is None:
        print(f"Error: No se pudieron cargar las imágenes. Verifica las rutas:")
        print(f"Imagen 1: {imagen1_path}")
        print(f"Imagen 2: {imagen2_path}")
        return None, 0
    
    # Verificar que las imágenes tienen el mismo tamaño
    if imagen1.shape != imagen2.shape:
        print("Las imágenes tienen diferentes dimensiones. Redimensionando...")
        imagen2 = cv2.resize(imagen2, (imagen1.shape[1], imagen1.shape[0]))
    
    # Crear copias para mostrar
    original = imagen1.copy()
    modificada = imagen2.copy()
    
    # Convertir a diferentes espacios de color para realizar múltiples comparaciones
    
    # 1. Comparación en RGB
    diferencia_rgb = cv2.absdiff(imagen1, imagen2)
    mascara_rgb = cv2.cvtColor(diferencia_rgb, cv2.COLOR_BGR2GRAY)
    _, mascara_rgb = cv2.threshold(mascara_rgb, sensibilidad, 255, cv2.THRESH_BINARY)
    
    # 2. Comparación en HSV (más sensible a cambios de color)
    hsv1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2HSV)
    diferencia_hsv = cv2.absdiff(hsv1, hsv2)
    mascara_hsv = cv2.cvtColor(diferencia_hsv, cv2.COLOR_BGR2GRAY)
    _, mascara_hsv = cv2.threshold(mascara_hsv, sensibilidad, 255, cv2.THRESH_BINARY)
    
    # 3. Combinar las máscaras para mayor precisión
    mascara_combinada = cv2.bitwise_or(mascara_rgb, mascara_hsv)
    
    # Preprocesamiento para eliminar ruido y mejorar detección
    kernel = np.ones((3, 3), np.uint8)
    mascara_combinada = cv2.morphologyEx(mascara_combinada, cv2.MORPH_OPEN, kernel, iterations=1)
    mascara_combinada = cv2.dilate(mascara_combinada, kernel, iterations=2)
    
    # Encontrar contornos de las áreas con cambios
    contornos, _ = cv2.findContours(mascara_combinada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Preparar imagen para mostrar diferencias
    imagen_diferencias = np.zeros_like(imagen1)
    cv2.drawContours(imagen_diferencias, contornos, -1, (0, 255, 0), -1)
    
    # Aplicar máscara para mostrar solo las diferencias reales
    imagen_diferencias_reales = cv2.bitwise_and(imagen2, imagen_diferencias)
    
    # Crear imagen resultado (copia de la imagen2)
    imagen_resultado = imagen2.copy()
    
    # Contar cambios significativos
    cambios_detectados = 0
    
    # Verificar cada contorno y dibujar rectángulos alrededor de los cambios
    for i, contorno in enumerate(contornos):
        area = cv2.contourArea(contorno)
        if area < area_minima:
            continue  # Ignorar contornos pequeños
        
        cambios_detectados += 1
        
        # Obtener rectángulo delimitador
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Añadir un poco de espacio alrededor del área detectada
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(imagen1.shape[1] - x, w + padding * 2)
        h = min(imagen1.shape[0] - y, h + padding * 2)
        
        # Dibujar rectángulo en la imagen resultado
        cv2.rectangle(imagen_resultado, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Añadir número de cambio
        cv2.putText(imagen_resultado, str(cambios_detectados), (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Crear una imagen de comparación lado a lado para este cambio específico
        recorte_original = original[y:y+h, x:x+w]
        recorte_modificado = modificada[y:y+h, x:x+w]
        
        # Redimensionar los recortes para mejor visualización si son muy pequeños
        min_size = 100
        if w < min_size or h < min_size:
            scale = max(min_size / w, min_size / h)
            new_w, new_h = int(w * scale), int(h * scale)
            recorte_original = cv2.resize(recorte_original, (new_w, new_h))
            recorte_modificado = cv2.resize(recorte_modificado, (new_w, new_h))
        
        # Guardar imágenes de recorte si se solicita
        if guardar:
            directorio = "cambios_detectados"
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            cv2.imwrite(f"{directorio}/cambio_{cambios_detectados}_original.jpg", recorte_original)
            cv2.imwrite(f"{directorio}/cambio_{cambios_detectados}_modificado.jpg", recorte_modificado)
    
    # Mostrar imágenes si se solicita
    if mostrar and cambios_detectados > 0:
        # Función auxiliar para redimensionar
        def resize_for_display(img, max_dim=800):
            h, w = img.shape[:2]
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                return cv2.resize(img, (int(w * scale), int(h * scale)))
            return img
        
        # Redimensionar para visualización
        original_resized = resize_for_display(original)
        modificada_resized = resize_for_display(modificada)
        resultado_resized = resize_for_display(imagen_resultado)
        
        # Crear visualización lado a lado
        h1, w1 = original_resized.shape[:2]
        h2, w2 = modificada_resized.shape[:2]
        
        # Crear imagen lado a lado para comparación
        comparison = np.zeros((max(h1, h2), w1 + w2, 3), dtype=np.uint8)
        comparison[:h1, :w1] = original_resized
        comparison[:h2, w1:w1+w2] = modificada_resized
        
        # Mostrar imágenes
        cv2.imshow("Original vs Modificada", comparison)
        cv2.imshow("Cambios Detectados", resultado_resized)
        
        print(f"Se detectaron {cambios_detectados} cambios.")
        print("Presiona cualquier tecla para cerrar las ventanas...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif mostrar and cambios_detectados == 0:
        print("No se detectaron cambios significativos entre las imágenes.")
    
    # Guardar imagen resultado
    if guardar:
        directorio = "cambios_detectados"
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        
        cv2.imwrite(f"{directorio}/resultado_completo.jpg", imagen_resultado)
        print(f"Imagen guardada en: {directorio}/resultado_completo.jpg")
    
    return imagen_resultado, cambios_detectados

def main():
    # MODIFICACIÓN: Usar rutas fijas en lugar de argumentos de línea de comandos
    # Rutas a las imágenes (modifica estas rutas según donde tengas tus imágenes)
    imagen1_path = "diferencias imagen 1.jpg"
    imagen2_path = "diferencias imagen 2.jpg"
    
    # Parámetros de detección
    sensibilidad = 10  # Valores más bajos = más sensible
    area_minima = 30   # Área mínima de los cambios a considerar
    mostrar = True     # Mostrar imágenes
    guardar = True     # Guardar resultados
    
    print("Iniciando detección de cambios con rutas fijas:")
    print(f"Imagen original: {imagen1_path}")
    print(f"Imagen modificada: {imagen2_path}")
    print(f"Sensibilidad: {sensibilidad}")
    print(f"Área mínima: {area_minima}")
    
    # Detectar cambios con los parámetros fijos
    detectar_cambios_ilustraciones(
        imagen1_path, 
        imagen2_path, 
        sensibilidad=sensibilidad, 
        area_minima=area_minima, 
        mostrar=mostrar, 
        guardar=guardar
    )

if __name__ == "__main__":
    main()