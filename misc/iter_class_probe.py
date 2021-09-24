class Itt:
    def __iter__ (self):
        print (f"итер сработал")
        for a in range(4):
            yield(a)


data = Itt()

for i in data:   # так не робит говорит что __iter__ не возвращает итератор
    # print (f"i {i}")
    pass

import array
import numpy as np

#array initialisation
array_arr= array.array('i',[1,2,3,4,5])
np_arr = np.array([6,7,8,9,10])

#slicing array with 1 parameter
# print("Sliced array: ", array_arr[:3])

a=np.ones((2,2,3))
b= np.reshape(a, (4,3))

print (b)
