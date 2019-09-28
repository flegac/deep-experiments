from typing import List

import numpy as np

from data_toolbox.data.data_mixer import DataMixer, Buffer


class CompareMixer(DataMixer):
    def apply(self, buffers: List[Buffer]) -> Buffer:
        if len(buffers) != 2:
            raise ValueError('Need exactly two masks to compare')

        true_labels, pred_labels = buffers
        true_labels=true_labels[:,:,0]
        pred_labels=pred_labels[:,:,0]

        TP = np.logical_and(pred_labels == 1, true_labels == 1)
        # TN = np.sum(np.logical_and(pred_labels == 0, true_labels == 0))
        FP = np.logical_and(pred_labels == 1, true_labels == 0)
        FN = np.logical_and(pred_labels == 0, true_labels == 1)

        return np.dstack([FN, TP, FP]).astype('uint8')
