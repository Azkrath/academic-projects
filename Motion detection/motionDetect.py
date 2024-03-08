# coding=utf-8
import cv2  # opencv3
from scipy.spatial.distance import euclidean

# BLOB - Grupo de pixeis conexos numa imagem que partilha propriedades identicas
class Blob(object):
    def __init__(self, center=(0, 0), rect=(0, 0, 0, 0), area=0, ratio=0.0):
        self.center = center
        self.rect = rect
        self.area = area
        self.ratio = ratio

# Obter o kernel / elementos estruturantes
def getKernel(x, y):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (x,y))

# Obter a posição dos centroides
def getCenter(cont):
    M = cv2.moments(cont)
    x = int(M['m10'] / M['m00'])
    y = int(M['m01'] / M['m00'])
    return x, y

# Applying the morphological filtering
def applyMorphEx(bs_mask1):
    # morphology
    bs_mask2 = cv2.morphologyEx(bs_mask1, cv2.MORPH_ERODE, getKernel(3, 3))
    bs_mask3 = cv2.morphologyEx(bs_mask2, cv2.MORPH_CLOSE, getKernel(12, 12))
    return bs_mask3

# Metodo de tracking
def Tracking(video, ini, fin):
    if ini >= fin:
        raise Exception("start frame must be less than end frame")

    # Variáveis
    blobs = [Blob()]
    font = cv2.FONT_HERSHEY_DUPLEX

    # Iniciar a captura de video
    videocap = cv2.VideoCapture(video)

    # Definir o framerate
    videocap.set(cv2.CAP_PROP_POS_FRAMES, ini)

    # Definir o algoritmo de subtração de background
    #bgsb = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=100, detectShadows=False)
    bgsb = cv2.createBackgroundSubtractorKNN(history=200, dist2Threshold=100, detectShadows=False)

    while videocap.isOpened:
        (ret, frame) = videocap.read()

        # Definir a frame com tons de cinzento
        gsframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar um filtro Gaussiano
        gbframe = cv2.GaussianBlur(gsframe, (3,3), 0)

        # Aplicar a subtração de background
        bs_mask1 = bgsb.apply(gbframe)

        # cv2.imshow('mask', bs_mask1)
        # cv2.imshow('track', frame)

        # Aplicar as transformações Morfológicas
        bs_mask = applyMorphEx(bs_mask1)

        # Obter os objetos ativos da imagem
        (im, contours, hierarchy) = cv2.findContours(bs_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Adicionar um novo contorno se o mesmo não existir na lista
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            exists = False
            if 150 < area < 10000:
                cx, cy = getCenter(cnt)
                for idx, blob in enumerate(blobs):
                    dist = euclidean(blob.center, (cx, cy))
                    if dist < 10:
                        exists = True
                if not exists:
                    new_blob = Blob((cx, cy), (x, y, w, h), area, aspect_ratio)
                    blobs.append(new_blob)

        # Se o contorno existe, atualizar a sua posição na lista
        # Se o contorno não existe, remover da lista
        for idx, blob in enumerate(blobs):
            updated = False
            for cnt in contours:
                area = cv2.contourArea(cnt)
                (x, y, w, h) = cv2.boundingRect(cnt)
                aspect_ratio = float(w) / h
                if 150 < area < 10000:
                    (cx, cy) = getCenter(cnt)
                    dist = euclidean(blob.center, (cx, cy))
                    if dist < 10:
                        blob.center = (cx, cy)
                        blob.rect = (x, y, w, h)
                        blob.area = area
                        blob.ratio = aspect_ratio
                        updated = True
            if not updated:
                blobs.pop(idx)

        # Desenhar os contornos
        # for k in range(0, len(contours)):
        #     cv2.drawContours(frame, contours, k, (0, 255, 0), 1)

        # cv2.imshow('mask', bs_mask)
        # cv2.imshow('track', frame)

        # Efetuar a classificação e desenhar o rectangulo
        id = 0
        for blob in blobs:
            id += 1
            (x, y, w, h) = blob.rect
            area = blob.area
            ratio = blob.ratio

            # Classificar o objecto em um dos tipos:
            # PESSOA
            if 150 < area < 2000 and ratio < 0.8:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, str(id), (x, y - 3), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA) # LINE_AA - Antialiasing para as linhas

            # CARRO
            elif 2000 < area < 10000 and ratio > 1.2:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, str(id), (x, y - 3), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA) # LINE_AA - Antialiasing para as linhas

            # OUTRO
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, str(id), (x, y - 3), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) # LINE_AA - Antialiasing para as linhas

        cv2.putText(frame, "Pessoa",( 10, int(videocap.get(4))-50 ), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA) # LINE_AA - Antialiasing para as linhas
        cv2.putText(frame, "Carro", ( 10, int(videocap.get(4))-35 ), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA) # LINE_AA - Antialiasing para as linhas
        cv2.putText(frame, "Outro", ( 10, int(videocap.get(4))-20 ), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA) # LINE_AA - Antialiasing para as linhas

        #cv2.imshow('mask', bs_mask)
        cv2.imshow('track', frame)

        if videocap.get(cv2.CAP_PROP_POS_FRAMES) >= fin or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videocap.release()
    cv2.destroyAllWindows()

# Main
ini = 0
fin = 3050 # FPS * Segundos de filme
video0 = "Videos/video0.avi"
video1 = Tracking(video0, ini, fin)