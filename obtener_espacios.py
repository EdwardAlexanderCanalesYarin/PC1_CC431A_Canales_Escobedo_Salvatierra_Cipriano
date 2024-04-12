
import cv2
import pickle

img = cv2.imread('cuadrados.png')

espacios = []

for x in range(29):
    #58 small (prueba)
    #29 big (cuadrados)
    espacio = cv2.selectROI('cuadrados', img, False)
    cv2.destroyWindow('cuadrados')
    espacios.append(espacio)

    for x, y, w, h in espacios:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

with open('prueba.pkl','wb') as file:
    pickle.dump(espacios, file)