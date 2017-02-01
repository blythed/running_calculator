import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
x = np.load('../completed_matrix_step_log_time.npy')
U,S,V = np.linalg.svd(x)
v = V[:3,:]
weights = np.dot(x,v.transpose())
spec = np.load('../specialization.npy')
merged = np.zeros((weights.shape[0],4))
merged[:,:3] = weights
merged[:,3] = np.log(spec)
df = pd.DataFrame(merged,columns=['w1', 'w2', 'w3', 'spec'])
np.save('../weights.npy',merged)
df.to_csv('../weights.csv')

