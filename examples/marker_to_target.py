#!/usr/bin/env python

import time
import cv2
import numpy as np
from lib import tracker

BLUE = (255, 50, 50)
GREEN = (50, 255, 50)
RED = (50, 50, 255)
WHITE = (255, 255, 255)


def put_text(img, text, pos, color):
    return cv2.putText(img, text, pos,
                       fontFace=cv2.FONT_HERSHEY_DUPLEX,
                       fontScale=0.6, color=color)


def main():
    target = (200, 200)
    radius = 80

    while True:
        start = time.time()
        __, img = cap.read()

        markers = tracker.find_markers(img)

        if 1 in markers:
            marker = markers[1]
            a = np.array(marker.major_axis)
            b = np.array(marker.position)
            c = np.array(target)
            phi = marker.angle_to_point(target)

            if np.linalg.norm(c - b) < radius - np.linalg.norm(b - a):
                contour_color = GREEN
            else:
                contour_color = RED

            if abs(phi) < 10:
                deg_color = GREEN
            else:
                deg_color = RED

            cv2.drawContours(img, [marker.contour], -1, contour_color, 2)
            cv2.line(img, marker.position, target, deg_color, 2)
            cv2.line(img, marker.position, marker.major_axis, WHITE, 2)
            cv2.circle(img, target, radius, contour_color, 2)
            put_text(img, 'Angle: {0}'.format(phi), (10, 40), deg_color)

        else:
            cv2.circle(img, target, radius, RED, 2)

        elapsed = time.time() - start
        put_text(img, 'FPS: {0}'.format(int(1 / elapsed)), (10, 20), RED)

        cv2.imshow('Main window', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    main()

    cap.release()
    cv2.destroyAllWindows()