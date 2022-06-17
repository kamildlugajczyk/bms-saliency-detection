import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm


def process(path):
    w0 = 5  # kernel size for opening operation (used after thresholding)
    d = 8  # step size for thresholding
    wd1 = 7  # dilation kernel size used for attention maps
    wd2 = 23  # dilation kernel size used in post-processing
    s = 9  # sigma -> standard deviation for gaussian filter in post-processing

    I = cv2.imread(path)
    # I = cv2.resize(I, (600, 400))
    B = []
    for k in range(3):
        for v in range(0, 256, d):
            B1 = cv2.threshold(I[:, :, k], v, 255, cv2.THRESH_BINARY)
            B2 = cv2.bitwise_not(B1[1], None)
            B.append(cv2.morphologyEx(B1[1], cv2.MORPH_OPEN, np.ones((w0, w0))))  # boolean map
            B.append(cv2.morphologyEx(B2, cv2.MORPH_OPEN, np.ones((w0, w0))))  # boolean map

    A_ = np.zeros_like(B[0])
    A = []
    for i in range(0, len(B)):
        x = cv2.floodFill(B[i], None, (0, 0), 0)
        for j in range(0, A_.shape[0], 16):
            x = cv2.floodFill(x[1], None, (0, j), 0)
            x = cv2.floodFill(x[1], None, (A_.shape[1] - 1, j), 0)
        for j in range(0, A_.shape[1], 16):
            x = cv2.floodFill(x[1], None, (j, A_.shape[0] - 1), 0)
            x = cv2.floodFill(x[1], None, (j, 0), 0)
        x = cv2.dilate(x[1], np.ones((wd1, wd1)))
        l2 = norm(x)
        x = np.array(x, dtype=np.float32)
        if (l2 != 0):
            x /= l2
        A_ = A_ + x
        A.append(x)
    A_ = A_ / len(B)  # Mean attention map

    result = cv2.dilate(A_, np.ones((wd2, wd2)))
    blur_width = np.int(np.min([np.floor(s * 4 + 1), 51]))
    result = cv2.GaussianBlur(result, (blur_width, blur_width), s)
    plt.axis('off')
    plt.imshow(result, cmap='gray')
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    return "result.jpg"
