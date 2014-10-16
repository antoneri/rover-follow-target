#!/usr/bin/env python

import cv2
from lib import tracker

BLUE = (255, 50, 50)
GREEN = (50, 255, 50)
RED = (50, 50, 255)
WHITE = (255, 255, 255)


def main():
    markers = tracker.find_markers(img)

    for m_id, marker in markers.iteritems():
        cv2.drawContours(img, [marker.contour], -1, GREEN, 2)
        cv2.line(img, marker.position, marker.major_axis, WHITE, 2)
        cv2.line(img, marker.position, marker.minor_axis, WHITE, 2)
        cv2.putText(img, str(marker), marker.position,
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.6, color=RED)


if __name__ == '__main__':
    STATIC = True

    if STATIC:
        img = cv2.imread('test.jpg')
        img = cv2.resize(img, None, fx=0.3, fy=0.3,
                         interpolation=cv2.INTER_LINEAR)

        main()

        cv2.imshow('Main window', img)
        cv2.waitKey(0)

    else:
        cap = cv2.VideoCapture(0)

        while True:
            __, img = cap.read()

            main()

            cv2.imshow('Main window', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    cv2.destroyAllWindows()
