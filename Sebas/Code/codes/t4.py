# -*- coding: latin-1 -*-
import cv2
import face_recognition
import os
import pickle

# Guardando el resultado de los encodings conocidos comprobando si ya existia antes
def run():
    pathing = "D:/Datos/Proyectos/Test1_Face_recognition/datapool/"
    # Comprobamos si el archivo ya existe:
    if not os.path.exists(pathing+'saved_encodings.dat'):
        # Cargamos todas las imagenes del datapool utilizando un bucle para recorrer las subcarpetas
        arrayImages = []
        faceEncodings = []
        i = 0
        pathfinal = os.listdir(pathing)
        for person in pathfinal:
            print(person)
            file = os.listdir(pathing + person)
            if (file.__len__() > 0):

                for imagen in file:
                    arrayImages.append(face_recognition.load_image_file(pathing + person + "/" + imagen))

                    # Para cada imagen generamos su encoding correspondiente
                    faceEncodings.append(face_recognition.face_encodings(arrayImages[i])[0])
                    i += 1

        with open(pathing+'saved_encodings.dat', 'wb') as f:
            pickle.dump(faceEncodings, f)
    else:
        with open(pathing+'saved_encodings.dat', 'rb') as f:
            faceEncodings = pickle.load(f)

    # Creamos un array con sus respectivos nombres:

    nombres_conocidos = [
        "Ben Afflek",
        "Albert Einstein",
        "Elton John",
        "Jerry Seinfeld",
        "Madonna",
        "Mindy Kailing",
        "Paul Langevin",
        "Max Planck",
    ]

    # Cargamos una fuente de texto:
    font = cv2.FONT_HERSHEY_COMPLEX

    # Cargamos la imagen donde hay que identificar los rostros:
    img = face_recognition.load_image_file('imagen_input.jpg')
    # (Para probar la segunda imagen hay que cambiar el argumento de la función por 'imagen_input2.jpg')

    # Definir tres arrays, que servirán para guardar los parámetros de los rostros que se encuentren en la imagen:
    loc_rostros = []  # Localizacion de los rostros en la imagen (contendrá las coordenadas de los recuadros que las contienen)
    encodings_rostros = []  # Encodings de los rostros
    nombres_rostros = []  # Nombre de la persona de cada rostro

    # Localizamos cada rostro de la imagen y extraemos sus encodings:
    loc_rostros = face_recognition.face_locations(img)
    encodings_rostros = face_recognition.face_encodings(img, loc_rostros)

    # Recorremos el array de encodings que hemos encontrado:
    for encoding in encodings_rostros:

        # Buscamos si hay alguna coincidencia con algún encoding conocido:
        coincidencias = face_recognition.compare_faces(faceEncodings, encoding, tolerance=0.6)

        # El array 'coincidencias' es ahora un array de booleanos.
        # Si contiene algun 'True', es que ha habido alguna coincidencia:
        if True in coincidencias:
            # Buscamos el nombre correspondiente en el array de nombres conocidos:
            encontrado = coincidencias.index(True)
            index = 0
            for carpeta in os.listdir(pathing):
                if (encontrado+1 - os.listdir(pathing+carpeta).__len__() <= 0):
                    nombre = nombres_conocidos[index]
                    break
                else:
                    index +=1
                    encontrado = encontrado - os.listdir(pathing+carpeta).__len__()

        # Si no hay ningún 'True' en el array 'coincidencias', no se ha podido identificar el rostro:
        else:
            nombre = "???"

        # Añadimos el nombre de la persona identificada en el array de nombres:
        nombres_rostros.append(nombre)

    # Dibujamos un recuadro rojo alrededor de los rostros desconocidos, y uno verde alrededor de los conocidos:
    for (top, right, bottom, left), nombre in zip(loc_rostros, nombres_rostros):

        # Cambiar el color segun el nombre:
        if nombre != "???":
            color = (0, 255, 0)  # Verde
        else:
            color = (0, 0, 255)  # Rojo

        # Dibujar los recuadros alrededor del rostro:
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)
        cv2.rectangle(img, (left, bottom - 20), (right, bottom), color, -1)

        # Escribir el nombre de la persona:
        cv2.putText(img, nombre, (left, bottom - 6), font, 0.6, (0, 0, 0), 1)

    # Abrimos una ventana con el resultado:
    cv2.imshow('Output', img)
    print("\nMostrando resultado. Pulsa cualquier tecla para salir.\n")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
