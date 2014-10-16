#!/usr/bin/env python

import time
import serial
import cv2
import numpy as np
from lib import tracker

BLUE = (255, 50, 50)
GREEN = (50, 255, 50)
RED = (50, 50, 255)
WHITE = (255, 255, 255)


class DummyTarget:
    def __init__(self, position):
        self.position = position


def put_text(img, text, pos, color):
    return cv2.putText(img, text, pos,
                       fontFace=cv2.FONT_HERSHEY_DUPLEX,
                       fontScale=0.6, color=color)


def main():
    target = DummyTarget((320, 240))
    radius = 80

    while True:
        start = time.time()
        __, img = cap.read()

        markers = tracker.find_markers(img)

        if 1 in markers:
            robot = markers[1]
            #target = markers[2]
            a, b, c = map(np.array, [robot.major_axis,
                                     robot.position,
                                     target.position])
            phi = robot.angle_to_point(target.position)

            if np.linalg.norm(c - b) < radius - np.linalg.norm(b - a):
                ser.write('x')  # stop if inside target radius
                contour_color = GREEN
                deg_color = GREEN
            else:
                contour_color = RED
                if abs(phi) < 15:
                    ser.write('w')  # forward
                    deg_color = GREEN
                elif phi > 0 or abs(phi) > 131:
                    ser.write('a')  # left
                    deg_color = RED
                elif -130 < phi < 0:
                    ser.write('d')  # right
                    deg_color = RED

            cv2.drawContours(img, [robot.contour], -1, contour_color, 2)
            cv2.line(img, robot.position, target.position, deg_color, 2)
            cv2.line(img, robot.position, robot.major_axis, WHITE, 2)
            cv2.line(img, robot.position, robot.minor_axis, WHITE, 2)
            cv2.circle(img, target.position, radius, contour_color, 2)
            put_text(img, 'Angle: {0}'.format(phi), (10, 40), deg_color)
        else:
            ser.write('x')  # stop

        elapsed = time.time() - start
        put_text(img, 'FPS: {0}'.format(int(1 / elapsed)), (10, 20), RED)

        cv2.imshow('Main window', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    serial_port = '/dev/tty.usbmodemfa141'
    try:
        ser = serial.Serial(serial_port, 9600)
    except OSError, msg:
        print msg
        raise SystemExit(0)

    time.sleep(2)

    main()

    cap.release()
    cv2.destroyAllWindows()
