#!/usr/bin/env python3

import cv2
import numpy as np
import logging
from networktables import NetworkTable
import time
import config
import subprocess
import math

from utils import camserver, const
from detect import detect

logging.basicConfig(level=logging.DEBUG)

def do_capture(self):
    if capture.isOpened():
        ret, frame = capture.read()
        if ret:
            img, cnt = (frame, 0)
            if ntable.getNumber("auto_enabled", 2) == const.VISION_COMMAND_ENABLED:
                img, cnt, __data = detect.do_detect(frame)
                push_data = {}
                cX, cY = (__data["cX"], __data["cY"])
                if cX is -1 and cY is -1:
                    push_data["cX"] = 0
                    push_data["cY"] = 0
                else:
                    push_data["cX"] = (cX - config.camera["cX"]) / config.camera["width"] * 2
                    push_data["cY"] = (cY - config.camera["cY"]) / config.camera["height"] * 2

                ntable.putNumber("target_angle", const.VISION_COMMAND_ENABLED)
                ntable.putNumber("robotdrive_status", const.VISION_COMMAND_ENABLED)
                ntable.putNumber("target_count_number", cnt)
                ntable.putNumber("target_angle_number", math.sqrt(math.pow(__data["cX"], 2) + math.pow(__data["cY"], 2)))
                ntable.putNumber("cX", push_data["cX"])
                ntable.putNumber("cY", push_data["cY"])

            if cnt == 0:
                ntable.putNumber("target_count", const.VISION_COMMAND_DISABLED)
            elif cnt == 1:
                ntable.putNumber("target_count", const.VISION_COMMAND_ENABLED)
            elif cnt >= 2:
                ntable.putNumber("target_count", const.VISION_COMMAND_IN_PROGRESS)

            return cv2.resize(img, (config.camera["r_width"], config.camera["r_height"]))
        else:
            return None
    else:
        return None

def get_device():
    # return "-d /dev/video%d" % (config.camera["id"])
    return ""

def onValueChanged(table, key, value, isNew):
    if key == "manual_exposure":
        if value == 0.0:
            subprocess.call("v4l2-ctl -c exposure_auto=1", shell=True)
            subprocess.call("v4l2-ctl -c exposure_absolute=5", shell=True)
        elif value == 2.0:
            subprocess.call("v4l2-ctl -c exposure_auto=3", shell=True)


def init_ntable():
    global ntable
    NetworkTable.setIPAddress(config.server["rioAddress"])
    NetworkTable.setClientMode()

    NetworkTable.initialize()

    ntable = NetworkTable.getTable('vision');

    ntable.addTableListener(onValueChanged)

def init_modules():
    subprocess.call("v4l2-ctl -c exposure_auto=3", shell=True)
    ntable.putNumber("auto_enabled", const.VISION_COMMAND_DISABLED);
    ntable.putNumber("manual_exposure", const.VISION_COMMAND_DISABLED);


def main():
    global capture
    init_ntable()
    init_modules()
    capture = cv2.VideoCapture(config.camera["id"])
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.camera["width"])
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.camera["height"])
    capture.set(cv2.CAP_PROP_FPS, config.camera["fps"])

    try:
        camserver.serve(config.server, do_capture)
    except KeyboardInterrupt:
        capture.release()

if __name__ == '__main__':
    main()
