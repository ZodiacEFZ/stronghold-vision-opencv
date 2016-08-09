import operator
import time
import cv2
import numpy as np

config_prev = {
    "hls": ([58,112,48], [105,255,152]),
    "bgr": ([96,78,0], [216,173,101])
}

config = {
    "hls": ([0,55,0], [180,255,255]),
    "bgr": ([0,0,0], [0,0,0])
}

def get_hls_image(img):
    # Hue Luminance Saturation
    lower = np.array(config["hls"][0])
    upper = np.array(config["hls"][1])
    return cv2.inRange(
        cv2.cvtColor(img, cv2.COLOR_BGR2HLS),
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
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h

        if w >= 10 and w <= 1000 and h >= 10 and h <= 300 and area >= 100 and hier[3] == -1 and solidity <= 0.60 \
            and 0.3 <= aspect_ratio and aspect_ratio <= 5:
            yield { "contour": cnt, "cx": cx, "cy": cy, "area": area, "solidity": solidity, "aspect_ratio": aspect_ratio }

def filter_target(contours, hierarchy):
    targets = list(filter_contours(contours, hierarchy))
    selected = []
    if len(targets) > 0:
        __target = min(targets, key=operator.itemgetter('solidity'))
        selected = filter(lambda t: abs(t["solidity"] - __target["solidity"]) <= 0.05, targets)
    return targets, selected

def do_detect(img):
    mask = get_hls_image(img)

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours, targets = filter_target(contours, hierarchy)

    contours = list(contours)
    targets = list(targets)
    __contours = list(map(operator.itemgetter("contour"), contours))
    __targets = list(map(operator.itemgetter("contour"), targets))

    cv2.drawContours(img, __contours, -1, (0, 255, 0), 3)
    cv2.drawContours(img, __targets, -1, (0, 0, 255), 3)

    data = { "cX": -1, "cY": -1 } if len(__targets) is 0 else {
        "cX": targets[0]["cx"],
        "cY": targets[0]["cy"]
    }

    return img, len(contours), data
