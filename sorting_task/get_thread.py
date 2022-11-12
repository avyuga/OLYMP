import cv2
import numpy as np
import matplotlib.pyplot as plt

# Возникающие проблемы:
# 1) как отделить винт от фона? (оба - оттенки серого, могут быть блики, плюс разный свет)
# 2) учесть разный размер изображений (приводить к одному пока что, хотя если съемк )

fig1, axes1 = plt.subplots(4, 7, constrained_layout=True)
fig1.set_figheight(12)
fig1.set_figwidth(24)

fig2, axes2 = plt.subplots(4, 7, constrained_layout=True)
fig2.set_figheight(12)
fig2.set_figwidth(24)

for i in range(28):
    name = f'D:\\DOCS\\PycharmProjects\\OLYMP\\sorting_task\\data\\thread_{(i + 1):03}.bmp'
    # name = f'D:\\DOCS\\PycharmProjects\\OLYMP\\sorting_task\\data\\thread_005.bmp'
    img = cv2.imread(name, cv2.IMREAD_UNCHANGED)

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

    # использование pic2 c усилением помогает для черных болтов
    # если сильно увеличивать pic1, то изображение начинает шуметь

    pic = (1.5*pic1 + 3*pic2).clip(0, 255)

    # cv2.imwrite(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\filter.jpeg', pic.astype(np.uint8))
    axes1[i // 7, i % 7].imshow(cv2.cvtColor(pic.astype(np.uint8), cv2.COLOR_BGR2RGB))
    axes1[i // 7, i % 7].set_title(f"{(i + 1):03}")

    mask = cv2.inRange(pic, (30, 30, 30), (255, 255, 255))

    b = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    c = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    d = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))

    res = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, b)
    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, c)
    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, d)

    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, b)
    axes2[i // 7, i % 7].imshow(cv2.cvtColor(res.astype(np.uint8), cv2.COLOR_BGR2RGB))
    axes2[i // 7, i % 7].set_title(f"{(i + 1):03}")

fig1.savefig(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\filter_all.jpeg')
fig2.savefig(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\mask_all.jpeg')

# res_thresh = cv2.bitwise_and(pic, pic, mask=dst.astype(np.uint8))
# cv2.imwrite(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\thresh.jpeg', mask)

# contours, hierarcy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contous = [i for i in contours if len(i) > 70]
# cnt = cv2.drawContours(pic, contours, -1, (0, 0, 255))
# cv2.imwrite(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\cnt.jpeg', cnt)