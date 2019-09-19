import cv2

from editor_api.data import DataOperator, Buffer


class EdgeDetectionOperator(DataOperator):

    def apply(self, data: Buffer) -> Buffer:
        # data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        # data = cv2.bilateralFilter(data, 11, 17, 17)
        edged = cv2.Canny(data, 0, 255)
        return edged
