import cv2
import pickle
import numpy as np

espacios = []
with open('prueba.pkl', 'rb') as file:
    espacios = pickle.load(file)

video = cv2.VideoCapture('video.mp4')

# Inicializar el contador de cuadros ocupados
full = 0

# Inicializar el estado de cada cuadro
estado = [False] * len(espacios)

while True:
    check, img = video.read()
    if not check:
        print('video terminado')
        break

    imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgTH, 5)
    kernel = np.ones((5, 5), np.int8)
    imgDil = cv2.dilate(imgMedian, kernel)

    for i, (x, y, w, h) in enumerate(espacios):
        espacio = imgDil[y:y+h, x:x+w]
        count = cv2.countNonZero(espacio)
        cv2.putText(img, str(count), (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if count >= 900:
            if not estado[i]:
                full += 1
                estado[i] = True
            # Cambié el color a azul para lugar ocupado
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)  
        else:
            if estado[i]:
                full -= 1
                estado[i] = False
            # Cuadro verde para lugar vacío    
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  

    # Mostrar el número de cuadros ocupados en el texto
    texto = f"Personas: {full}"
    cv2.putText(img, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow('video', img)
    cv2.waitKey(10)
