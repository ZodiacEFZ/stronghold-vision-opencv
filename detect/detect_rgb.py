import operator
import time
import cv2
import numpy as np

config = {
    "hsv": ([65,39,55], [95,255,180]),
    "rgb": [
        ([11,78,105], [101,186,201]),
        ([69,128,144], [150,176,191]),
        ([0,105,110], [75,158,161])
    ]
}

def get_hsv_image(img, crange):
    # Hue Luminance Saturation
    lower = np.array(crange[0])
    upper = np.array(crange[1])
    return cv2.inRange(
        cv2.cvtColor(img, cv2.COLOR_BGR2HSV),
        lower, upper
    )

def get_rgb_image(img, crange):
    # Hue Luminance Saturation
    lower = np.array(crange[0])
    upper = np.array(crange[1])
    return cv2.inRange(
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
        lower, upper
    )

def filter_contours(contours, hierarchy):
    for cnt, hier in zip(contours, hierarchy[0]):
        M = cv2.moments(cnt)

        if M['m00'] == 0:
            continue

        cx = M['m10']/M['m00']
        cy = M['m01']/M['m00']
        area = cv2.contourArea(cnt)

        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h

        if cx >= 30 and cx <= 1000 and cy >= 0 and cy <= 600 and area >= 80 and hier[3] == -1 and solidity <= 0.49 \
        and 0.3 <= aspect_ratio and aspect_ratio <= 5:
            yield { "contour": cnt, "cx": cx, "cy": cy, "area": area, "solidity": solidity, "aspect_ratio": aspect_ratio }

def filter_target(contours, hierarchy):
    targets = list(filter_contours(contours, hierarchy))
    selected = []
    if len(targets) > 0:
        __target = min(targets, key=operator.itemgetter('solidity'))
        selected = filter(lambda t: abs(t["solidity"] - __target["solidity"]) <= 0.05, targets)
    return list(map(operator.itemgetter("contour"), targets),), list(map(operator.itemgetter("contour"), selected))

def do_detect(img):

    mask = get_hsv_image(img, config["hsv"])
    for cfilter in config["rgb"]:
        __mask = get_rgb_image(img, cfilter)
        mask = cv2.bitwise_or(mask, __mask)

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours, targets = filter_target(contours, hierarchy)

    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.drawContours(img, targets, -1, (0,0,255), 3)

    return img, len(contours)
