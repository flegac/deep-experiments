import cv2
import imutils

from editor_api.data import DataOperator, Buffer


class ShowContours(DataOperator):

    def apply(self, data: Buffer) -> Buffer:
        # gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        # gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(data, 0, 255)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:]
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            cv2.drawContours(data, [approx], -1, color=(0, 255, 0), thickness=1)
        return data
