import numpy as np


def invert(value):
    if value == 1:
        return 0
    else:
        assert value == 0
        return 1


def index2direction(value):
    if value == 0:
        return -1
    else:
        assert value == 1
        return value


lightmap = np.random.randn(2, 2, 2)
lm = lightmap.max()  # 最大值
index = np.unravel_index(lightmap.argmax(), lightmap.shape)
adj_x_index = (invert(index[0]),) + index[1:3]
adj_y_index = (index[0],) + (invert(index[1]),) + (index[2],)
adj_z_index = index[0:2] + (invert(index[2]),)
adj_x = lightmap[adj_x_index]
adj_y = lightmap[adj_y_index]
adj_z = lightmap[adj_z_index]
dx = lm - adj_x
dy = lm - adj_y
dz = lm - adj_z
light_value = np.array([dx, dy, dz])
direction_vec = np.array(
    [
        index2direction(index[0]),
        index2direction(index[1]),
        index2direction(index[2])
    ]
)
light_vec = direction_vec * light_value
print('Done')
