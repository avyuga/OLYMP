import cv2
import numpy as np
import pyzed.sl as sl

def define_color(color):
    if color[2] > color[1] and color[2] > color[0] and color[2] > 50:
        return "RED"
    if color[0] > color[2] and color[0] > color[1] and color[0] > 50:
        return "BLUE"
    return "NONE"

def mask(img):
    """
    Определяем фон (как самую серую часть), с помощью маски удаляем её
    Также в этом же фильтре, отсекая менее яркие участки цвета,
    расширяем границы между близко лежащими блоками,
    чтобы определитель контуров их засекал
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array((0, 150, 70), np.uint8)
    hsv_max = np.array((255, 255, 255), np.uint8)
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    cv2.imwrite('C:/Users/Anastasia/Documents/ZED/pictures/thresh_init.png', thresh)
    return cv2.bitwise_and(img, img, mask=thresh)


def find_colored_contours(img):
    thresh_red = cv2.inRange(img, (0, 0, 90), (255, 255, 255))
    thresh_blue = cv2.inRange(img, (100, 0, 0), (255, 255, 255))
    red_contours, _ = cv2.findContours(
        thresh_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(
        thresh_blue, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return red_contours + blue_contours


def cyber_vision(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    masked_image = mask(img)
    cv2.imwrite('C:/Users/Anastasia/Documents/ZED/pictures/masked_image.png', masked_image)

    contours = find_colored_contours(masked_image)

    contours_img = masked_image.copy()
    contours_img = cv2.drawContours(contours_img, contours, -1, (0, 0, 255), 2)
    cv2.imwrite('C:/Users/Anastasia/Documents/ZED/pictures/contours.png', contours_img)

    i = 0
    for cnt in contours:
        circle = cv2.minEnclosingCircle(cnt)
        center_x = int(circle[0][0])
        center_y = int(circle[0][1])
        radius = int(circle[1])

        if radius > 40:
            print("Color: ", define_color(img[center_y][center_x]), " ", img[center_y][center_x])
            cv2.circle(masked_image, (center_x, center_y), 10, (10 + i * 60, 255, 255), 5)
            print('Center at ({0:f}, {1:f})   Radius: {2:f}'.format(center_x, center_y, radius))
            cv2.circle(masked_image, (center_x, center_y), radius, (0, 255, 0), 3)
            i += 1

    cv2.imwrite('C:/Users/Anastasia/Documents/ZED/pictures/new_circles.png', masked_image)

def get_image(camera: sl.Camera):
    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    if camera.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        camera.retrieve_image(image, sl.VIEW.LEFT)
        timestamp = camera.get_timestamp(sl.TIME_REFERENCE.CURRENT)
        print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(),
                                                                             image.get_height(),
                                                                             timestamp.get_milliseconds()))

    img = image.get_data()
    cv2.imwrite('C:/Users/Anastasia/Documents/ZED/pictures/circles.png', img)
    return img
