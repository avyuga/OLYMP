import cv2
import numpy as np
import matplotlib.pyplot as plt
from sorting_task.filters import morph, mask, double_gradient


fig1, axes1 = plt.subplots(4, 7, constrained_layout=True)
fig1.set_figheight(12)
fig1.set_figwidth(24)

fig2, axes2 = plt.subplots(4, 7, constrained_layout=True)
fig2.set_figheight(12)
fig2.set_figwidth(24)

for i in range(28):
    name = f'D:\\DOCS\\PycharmProjects\\OLYMP\\sorting_task\\data\\thread_{(i + 1):03}.bmp'
    pic = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    res = morph(mask(pic))

    d_grad = double_gradient(res).astype(np.uint8)
    axes2[i // 7, i % 7].imshow(res, cmap='gray', vmin=0, vmax=255)
    axes2[i // 7, i % 7].set_title(f"{(i + 1):03}")

    contours, _ = cv2.findContours(d_grad, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = [i for i in contours if i.shape[0] > 1000]
    cnt = sorted(cnt, key=len)

    img = cv2.cvtColor(d_grad, cv2.COLOR_GRAY2RGB)

    for contour in cnt:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        dim1 = np.linalg.norm(box[1] - box[0])
        dim2 = np.linalg.norm(box[2] - box[1])
        if dim2 > dim1:
            pt1 = (box[1] + box[0]) // 2
            pt2 = (box[2] + box[3]) // 2
        else:
            pt1 = (box[1] + box[2]) // 2
            pt2 = (box[0] + box[3]) // 2
        d_grad = cv2.line(d_grad, pt1, pt2, (0, 0, 0), thickness=20)

        contours, _ = cv2.findContours(d_grad, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = [i for i in contours if i.shape[0] > 750]
        cnt = sorted(cnt, key=len)
        img = cv2.cvtColor(d_grad, cv2.COLOR_GRAY2RGB)
        img = cv2.drawContours(img, cnt, -1, (0, 255, 0), thickness=1)

    axes1[i // 7, i % 7].imshow(img)
    axes1[i // 7, i % 7].set_title(f"{(i + 1):03}")

fig1.suptitle("res")
fig2.suptitle("mask")

fig1.show()
fig2.show()
# fig2.savefig(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\one_side.jpeg')

# num = len(cnt)-2
# fig, axes = plt.subplots()
# data = cnt[num].squeeze().T
# _, k = data.shape
# data1 = data[:, :k//2]
# data2 = data[:, k//2:]
# axes.plot(data1[0], data1[1], color='red', alpha=0.5)
# axes.plot(data2[0], data2[1], color='green', alpha=0.5)
# axes.invert_yaxis()
# fig.show()


# fig1.savefig(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\double_grads_all.jpeg')

# res_thresh = cv2.bitwise_and(pic, pic, mask=dst.astype(np.uint8))
# cv2.imwrite(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\thresh.jpeg', mask)

# contours, hierarcy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contous = [i for i in contours if len(i) > 70]
# cnt = cv2.drawContours(pic, contours, -1, (0, 0, 255))
# cv2.imwrite(r'D:\DOCS\PycharmProjects\OLYMP\sorting_task\images\cnt.jpeg', cnt)