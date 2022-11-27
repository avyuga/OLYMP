import cv2
import numpy as np


def gradient_filter(img, k1, k2):

    G_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    G_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    img_x = cv2.filter2D(img, -1, G_x)
    img_y = cv2.filter2D(img, -1, G_y)
    pic1 = cv2.magnitude(img_x.astype(np.float32), img_y.astype(np.float32))

    G_x = np.array([[1, -1], [0, 0]])
    G_y = np.array([[1, 0], [-1, 0]])
    img_x = cv2.filter2D(img, -1, G_x)
    img_y = cv2.filter2D(img, -1, G_y)
    pic2 = cv2.magnitude(img_x.astype(np.float32), img_y.astype(np.float32))

    pic = (k1 * pic1 + k2 * pic2).clip(0, 255)
    return pic


# ----------- Morphological skeleton ----------- #
def mask(img):
    f = gradient_filter(img, k1=1.5, k2=3)
    f = f.astype(np.uint8)
    # бинаризация градиента изображения позволяет получить контур,
    # а затем морфорлогия исправляет все дефекты
    mask = cv2.inRange(f, (30, 30, 30), (255, 255, 255))
    find_mean = cv2.bitwise_and(img, img, mask=mask)
    pixel_mean = np.mean(find_mean, axis=(0, 1))
    if np.mean(pixel_mean) < 6:
        mask = cv2.inRange(img, (0, 0, 0), (70, 70, 70))
    return mask


# вызывается для маски, чтобы зачистить её от дефектов!
def morph(img):
    b = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    c = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))

    res = cv2.morphologyEx(img, cv2.MORPH_CLOSE, b)
    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, c)
    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, d)

    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, b)
    return res


def double_gradient(img):
    return gradient_filter(img, k1=15, k2=15).astype(np.uint8)


def get_skeleton(img):
    pic_gradient = double_gradient(img)
    _, pic = cv2.threshold(pic_gradient, 250, 255, cv2.THRESH_BINARY)

    elem = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skeleton = np.zeros(pic.shape, dtype=np.uint8)
    counter = 0

    pic = pic.astype(np.uint8)
    while True:
        counter += 1
        temp = cv2.morphologyEx(pic, cv2.MORPH_OPEN, elem)
        temp = cv2.bitwise_not(temp)
        temp = cv2.bitwise_and(pic, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        pic = cv2.erode(pic, elem)

        if cv2.minMaxLoc(pic)[1] == 0: break
        # аварийный счетчик
        if counter == 300: break
    return skeleton
