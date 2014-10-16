import cv2
import numpy as np


class Marker:
    """Marker class which gets designated to all valid markers"""

    def __init__(self, marker_id, contour, polygon, rotations=0):
        self.id = marker_id
        self.contour = contour
        self.polygon = polygon
        self.rotations = rotations

        self.cx, self.cy = self.position
        self.x, self.y = self.corners

    def __str__(self):
        return str(self.id)

    @property
    def position(self):
        m = cv2.moments(self.contour)
        x = int(m['m10']/m['m00'])
        y = int(m['m01']/m['m00'])
        return x, y

    @property
    def corners(self):
        x, y = map(np.squeeze, np.hsplit(np.squeeze(self.polygon), 2))
        return x, y

    @property
    def major_axis(self):
        r = self.rotations
        f = lambda z: z[(4-r) % 4] + int((z[(5-r) % 4] - z[(4-r) % 4]) / 2)
        x, y = map(f, [self.x, self.y])
        return x, y

    @property
    def minor_axis(self):
        r = self.rotations
        f = lambda z: z[(5-r) % 4] + int((z[(6-r) % 4] - z[(5-r) % 4]) / 2)
        x, y = map(f, [self.x, self.y])
        return x, y

    @property
    def area_vec(self):
        raise NotImplementedError

    def angle_to_point(self, pt):
        maj, pos, pt = map(np.array, [self.major_axis, self.position, pt])

        phi = np.arctan2(*(maj - pos))
        rho = np.arctan2(*(pt - pos))

        f = lambda x: x + 2*np.pi if x < 0 else x
        phi, rho = map(f, [phi, rho])

        return round(np.degrees(rho - phi))