import numpy as np
a = np.ones([10, 1])
b = np.zeros([10, 1])
b[1] += 1
print(np.size(b, 1))
c = b == 0
print(c)
