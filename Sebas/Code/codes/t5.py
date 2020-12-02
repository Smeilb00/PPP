# -*- coding: latin-1 -*-
import cv2
import face_recognition
import os
import pickle


def run():
    print("Sistema de reconocimiento facial T5")
    arrayImages = []
    path = os.getcwd()
    pathinghome = path + "\datapool"
    if not os.path.exists(path + '\output\saved_encodings.dat'):
        faceEncodings = encoding_generator(arrayImages, pathinghome)
        print("Generados encodings para " + " imágenes en total.")
    else:
        with open(path + '\output\saved_encodings.dat', 'rb') as f:
            faceEncodings = pickle.load(f)

    # Definimos la lista de nombres conocidos con el siguiente método
    nombres_conocidos = namelist_generator(os.listdir(pathinghome))

    # Necesitamos una fuente para escribir el recuadro
    font = cv2.FONT_HERSHEY_COMPLEX

    # La imagen donde se buscan las caras por ahora se carga directamente
    img = face_recognition.load_image_file(path + '\input\imagen_input.jpg')

    # Generamos los 3 arrays para los parámetros de los rostros de la imagen
    loc_rostros = face_recognition.face_locations(img)
    encoding_rostros = face_recognition.face_encodings(img, loc_rostros)

    # LLamamos al método que compara las caras encontradas con las que tenia almacenadas
    nombres_rostros = finding_faces(pathinghome, encoding_rostros, faceEncodings)

    # Dibujamos los cuadrados al rededor
    draw_squares(img, font, loc_rostros, nombres_rostros)

    # Abrimos una ventana con el resultado:
    cv2.imshow('Output', img)
    cv2.imwrite(path + '\output\Output.jpg', img)
    print("\nMostrando resultado. Pulsa cualquier tecla para salir.\n")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def encoding_generator(arrayimages, pathinghome):
    # Este método se encarga de generar el encoding de cada cara
    # y lo exporta a un archivo .dat
    faceEncodings = []
    i = 0
    pathfinal = os.listdir(pathinghome)
    for person in pathfinal:
        file = os.listdir(pathinghome + person)
        if (file.__len__() > 0):
            for imagen in file:
                arrayimages.append(face_recognition.load_image_file(pathinghome + person + "/" + imagen))

                # Para cada imagen generamos su encoding correspondiente
                faceEncodings.append(face_recognition.face_encodings(arrayimages[i])[0])
                i += 1

    with open(path + '\output\saved_encodings.dat', 'wb') as f:
        pickle.dump(faceEncodings, f)
    return faceEncodings

def namelist_generator(directorylist):
    # Este método genera una lista de nombres conocidos en función de
    # las carpetas existentes en la carpeta raíz datapool
    namelist = []
    for carpeta in directorylist:
        namelist.append(carpeta)
    print("Se ha generado una lista de nombres conocidos")

    return namelist


def finding_faces(pathinghome, encoding_rostros, faceencodings):
    nombres_rostros = []
    for encoding in encoding_rostros:
        # Array de Trues y Falses en funcion de si encuentra las caras en las que ya conoce
        coincidencias = face_recognition.compare_faces(faceencodings, encoding, tolerance=0.5)

        if True in coincidencias:
            encontrado = coincidencias.index(True)
            index = 0
            for carpeta in os.listdir(pathinghome):
                if not os.path.isfile(carpeta):
                    encontrado = encontrado - os.listdir(pathinghome+"\\"+carpeta).__len__()
                    if encontrado < 0:
                        nombre = carpeta.__str__()
                        break
        else:
            nombre = "???"

        nombres_rostros.append(nombre)

    return nombres_rostros


def draw_squares(img, font, loc_rostros, nombres_rostros):
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