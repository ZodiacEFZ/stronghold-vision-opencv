#!/usr/bin/env python3

import operator
import time
import cv2
import numpy as np
import os
from matplotlib import pyplot

from detect import detect

MAX_RANGE = 543

def drawHist(data):
    pyplot.hist(data, 30, facecolor='green', alpha=0.5)
    pyplot.xlabel('Target')
    pyplot.ylabel('Frequency')
    pyplot.title('Vision Process')
    pyplot.show()

def main():
    data = []

    __path = "TestData/RealFullField"
    __time = time.clock()
    __cnt = 0

    for (dirpath, dirnames, filenames) in os.walk(__path):
        for path in filenames:
            img = cv2.imread("%s/%s" % (__path, path))

            if not img is None:
                # img = cv2.resize(img, (1280, 720))

                img, cnt, __data = detect.do_detect(img)
                
                cv2.imwrite("TestData/Result/%s" % path, img)

                print("%d/%d" % (__cnt + 1, len(filenames)))

                data.append(cnt)
                __cnt = __cnt + 1


    __elapsed = time.clock() - __time


    print("%d images analyzed within %f seconds, avg %f, %f/s" % (__cnt, __elapsed, __elapsed / __cnt, __cnt / __elapsed))

    drawHist(data)

if __name__ == '__main__':
    main()
