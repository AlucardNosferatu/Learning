import tensorflow.keras.backend as K
import tensorflow as tf
from Config import CheckLoss
from tensorflow.keras.losses import Loss


def ROILoss(y_true, y_pred):
    if CheckLoss:
        tf.print()
        tf.print(y_true)
        tf.print(y_pred)
    x_left = K.maximum(y_true[:, 0], y_pred[:, 0])
    y_top = K.maximum(y_true[:, 1], y_pred[:, 1])
    x_right = K.minimum(y_true[:, 2], y_pred[:, 2])
    y_bottom = K.minimum(y_true[:, 3], y_pred[:, 3])
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    bb1_area = (y_true[:, 2] - y_true[:, 0]) * (y_true[:, 3] - y_true[:, 1])
    bb2_area = (y_pred[:, 2] - y_pred[:, 0]) * (y_pred[:, 3] - y_pred[:, 1])
    iou = intersection_area / (bb1_area + bb2_area - intersection_area)
    result = tf.where(
        tf.math.logical_or(
            K.less(x_right, x_left),
            K.less(y_bottom, y_top)
        ),
        K.mean(K.square(y_true - y_pred), axis=-1)/1000,
        1 - iou
    )
    if CheckLoss:
        tf.print(result)
    return result
