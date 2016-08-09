#!/usr/bin/env python3

import operator
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

MAX_RANGE = 543

sift = cv2.xfeatures2d.SIFT_create()
orb = cv2.xfeatures2d.SIFT_create()
bf = cv2.BFMatcher()

imgT = cv2.imread("TestData/Target/TowerTargetW.jpg", 0)

kpT, desT = sift.detectAndCompute(imgT, None)

__time = time.clock()
__cnt = 0

for i in range(MAX_RANGE):
    img = cv2.imread("TestData/RealFullField/%d.jpg" % (i))

    if not img is None:
        kp, des = sift.detectAndCompute(img, None)

        matches = bf.knnMatch(desT, des, k=2)

        good = []

        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        result = cv2.drawMatchesKnn(img, kp, imgT, kpT, good, None, flags=2)


        cv2.imwrite("TestData/Result/res%d.png" % (i), result)

        print("%d/%d" % (i + 1, MAX_RANGE))

        __cnt = __cnt + 1

__elapsed = time.clock() - __time


print("%d images analyzed within %f seconds, avg %f, %f/s" % (__cnt, __elapsed, __elapsed / __cnt, __cnt / __elapsed))
