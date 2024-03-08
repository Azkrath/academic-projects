import cv2
import numpy as np
import random
from matplotlib import pyplot as plt

# Histogram calculation
def drawHistGray(img, mask, size, range):
    plt.figure(1)
    hist = cv2.calcHist([img], [0], mask, size, range)
    plt.plot(hist, color = 'gray')
    plt.xlim(range)
    plt.title("Image Histogram Gray")

def drawHistColor(img, mask, size, range):
    color = ('blue','green','red')
    plt.figure(2)
    for i,col in enumerate(color):
        hist = cv2.calcHist([img], [i], mask, size, range)
        plt.plot(hist, color = col)
        plt.xlim(range)
    plt.title("Image Histogram Color")

def drawHistograms(img, mask, size, range):
    drawHistGray(img, mask, size, range)
    drawHistColor(img, mask, size, range)
    plt.show()

# Define coin properties
def getCoinProps():
    coin_1e =  np.array([100,              # value
                         1.95674285e+04,    # area
                         5.2426431e+02,     # perimeter
                         1.11779194e+00])   # circularity
    coin_50c = np.array([50,
                         2.13256666e+04,
                         5.47310048e+02,
                         1.11778439e+00])
    coin_20c = np.array([20,
                         1.76373571e+04,
                         4.97752778e+02,
                         1.11787197e+00])
    coin_10c = np.array([10,
                         1.38530000e+04,
                         4.41217456e+02,
                         1.11829086e+00])
    coin_5c =  np.array([5,
                         1.58832500e+04,
                         4.72138127e+02,
                         1.11683721e+00])
    coin_2c =  np.array([2,
                         1.26150000e+04,
                         4.21003773e+02,
                         1.11809899e+00])
    coin_1c =  np.array([1,
                         8.97316666e+03,
                         3.55948265e+02,
                         1.12364195e+00])

    return np.array([coin_1c,coin_2c,coin_5c,coin_10c,coin_20c,coin_50c,coin_1e])

def getValue(d):
    if d < 100:
        return d / 100, str(int(d)) + ' cent'
    else:
        return d / 100, str(int(d) / 100) + ' euro'

def coinCenter(cont):
    M = cv2.moments(cont)
    x = int(M['m10'] / M['m00'])
    y = int(M['m01'] / M['m00'])
    return x, y

# make image plot
def plotImage(img, title):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyWindow(title)

# get the coin contours
def getContours(img):
    return cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# get the coin properties
def getProperties(cnt):
    # get Moments
    M = cv2.moments(cnt)
    # print M
    # print type(M['mu02'])

    # get Area
    A = cv2.contourArea(cnt)
    # print A

    # get Perimeter
    P = cv2.arcLength(cnt, True)
    # print P

    # get Circularity  -[ C = p^2 / 2pi*A ]
    C = (P**2)/(4*np.pi*A)
    # print C

    # get Eccentricity (not used)
    # E = ((M['mu20'] - M['mu02'])**2 - 4*M['mu11']**2) / (M['mu20'] + M['mu02'])**2
    # print M['mu20']
    # print M['mu02']
    # print M['mu11']
    # print E

    return np.array([A, P, C])

# Applying the morphological filtering
def applyMorphEx(img_thr):
    # plotImage(img_thr, "Binary Image")
    img_strut1 = cv2.morphologyEx(img_thr, cv2.MORPH_DILATE, getKernel(7,7))
    # plotImage(img_strut1, "Dilated Image")
    img_strut2 = cv2.morphologyEx(img_strut1, cv2.MORPH_ERODE, getKernel(117, 117))
    # plotImage(img_strut2, "Eroded Image")
    img_strut3 = cv2.morphologyEx(img_strut2, cv2.MORPH_DILATE, getKernel(105, 105))
    # plotImage(img_strut3, "Final Image")
    return img_strut3

# get the structuring elements or kernel
def getKernel(x, y):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (x,y))

# make the binarization of the image
def binarization(img):
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    # img_blue = cv2.split(img)[0] # Costly Operation
    # img_blue = img[:,:,0]
    # img_green = cv2.split(img)[1] # Costly Operation
    # img_green = img[:,:,1]
    # img_red = cv2.split(img)[2] # Costly Operation
    img_red = img[:,:,2]
    # img_blur = cv2.medianBlur(img_red, 3)
    img_blur = cv2.GaussianBlur(img_red, (1,1), 0)
    ret, img_thr = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # plotImage(img_gray, "Gray Image")
    # plotImage(img_blue, "Blue Image")
    # plotImage(img_green, "Green Image")
    # plotImage(img_red, "Red Image")
    # plotImage(img_blur, "Blur Image")
    # plotImage(img_thr, "Otsu Image")
    return img_thr


# Test
# img_src = cv2.imread("Images\img9.jpg")
# img_bin = binarization(img_src)
# img_strut = applyMorphEx(img_bin)
# img = img_strut.copy()
# contours, hierarchy = getContours(img)
# for i in range(0, len(contours)):
#     cnt = contours[i]
#     P = getProperties(cnt)
#     x, y = coinCenter(cnt)
#     cv2.putText(img_src, np.array_str(P), (x + 10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#     print P
#plotImage(img_strut, "Binary Image")
#plotImage(img_src, "Orig Image")

# Main
coins = ["Images\img1.jpg", "Images\img2.jpg", "Images\img3.jpg", "Images\img4.jpg", "Images\img5.jpg",
         "Images\img6.jpg", "Images\img7.jpg", "Images\img8.jpg", "Images\img9.jpg", "Images\img10.jpg", "Images\img11.jpg", "Images\img12.jpg",
         "Images\img13.jpg", "Images\img14.jpg"]
coins1 = ["Images\img10.jpg", "Images\img13.jpg", "Images\img14.jpg"]

for i in range(0, len(coins)):
    img = cv2.imread(coins[i])
    # drawHistograms(img, None, [256], [0, 256])
    img_bin = binarization(img)
    img_strut = applyMorphEx(img_bin)
    bw = img_strut.copy()
    contours, hierarchy = getContours(bw)
    total = 0.0
    distance = 650

    coinProps = getCoinProps()
    for j in range(0, len(coinProps)):
        A = coinProps[j][1:]
        value, text = getValue(coinProps[j][0])

        for k in range(0, len(contours)):
            cnt = contours[k]
            B = getProperties(cnt)
            dst = np.linalg.norm(A-B)
            if dst < distance:
                total += value
                x, y = coinCenter(cnt)
                color = (random.randrange(0, 257, 10),random.randrange(0, 257, 10),random.randrange(0, 257, 10))
                cv2.drawContours(img, contours, k, color, 3)
                cv2.putText(img, text, (x + 10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    if total > 0:
        cv2.putText(img, 'Total: ' + str(total) + ' euros', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    plotImage(img, "Orig Image")