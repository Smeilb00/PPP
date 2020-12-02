import cv2
def run():
    # Cargamos nuestro classificador de Haar:
    cascada_rostro = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    # Si utilizas otro clasificador o lo tienes guardado en un directorio diferente al de este script python,
    # tendrás que cambiar 'haarcascade_frontalface_alt.xml' por el path a tu fichero xml.

    # Cargamos la imagen y la convertimos a grises:
    img = cv2.imread('imagen_input.jpg')
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Nota: la imagen de ejemplo que hemos utilizado para el tutorial ya está en blanco y negro,
    # por lo que no sería necesario convertirla. Lo he hecho igualmente por si más adelante queréis
    # probar con una imagen en color.

    # Buscamos los rostros:
    coordenadas_rostros = cascada_rostro.detectMultiScale(img_gris, 1.3, 5)
    # Nota 1: la función detectMultiScale() requiere una imagen en escala de grises. Esta es la razón
    # por la que hemos hecho la conversión de BGR a Grayscale.
    # Nota 2: '1.3' y '5' son parámetros estándar para esta función. El primero es el factor de escala ('scaleFactor'): la
    # función intentará encontrar rostros escalando la imagen varias veces, y este factor indica en cuánto se reduce la imagen
    # cada vez. El segundo parámetro se llama 'minNeighbours' e indica la calidad de las detecciones: un valor elevado
    # resulta en menos detecciones pero con más fiabilidad.

    # Ahora recorremos el array 'coordenadas_rostros' y dibujamos los rectángulos sobre la imagen original:
    for (x, y, ancho, alto) in coordenadas_rostros:
        cv2.rectangle(img, (x, y), (x + ancho, y + alto), (0, 0, 255), 3)

    # Abrimos una ventana con el resultado:
    cv2.imshow('Output', img)
    print("\nMostrando resultado. Pulsa cualquier tecla para salir.\n")
    cv2.waitKey(0)
    cv2.destroyAllWindows()