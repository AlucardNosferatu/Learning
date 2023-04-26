# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 11:19:46 2019

@author: 16413
"""

import numpy as np
import pandas as pd

acc = pd.DataFrame(np.load("LP\\1\\acc.npy"))
loss = pd.DataFrame(np.load("LP\\1\\loss.npy"))

acc.plot(figsize=(20,5))
loss.plot(figsize=(20,5))