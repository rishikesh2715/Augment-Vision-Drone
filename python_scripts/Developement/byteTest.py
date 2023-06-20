import numpy as np

a = np.array(([109,15]), dtype=np.uint8)
b = np.ndarray((1,), dtype=np.uint16, buffer=a)
print(b*0.0062)
c = b.byteswap()
print(c)
print(c*0.0062)