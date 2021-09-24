a= ["wer3", "dfr3", "nj3u"]
sw = [i for i in a if f"er{3}" in i]
# print (f"sw{sw}")

l1 = [[[],[]],[[],[]],[[],[]]]
# print (f"len {len(l1)}")            # 3
from os import pipe
import numpy as np 
ln1 = np.array(l1)
# print (f"ln1 shape {ln1.shape}")    # (3,2,0)
# print (f"ln1 len {len(ln1)}")       # 3

asd = [10e1000]
l = 1
if l< min(asd):
    asd.append(l)
    # print (f"min {min(asd)} asd {asd}")

a,s,w,r,e = 0,0,0,0,0
a=1
# print (f"a{ a}")

class Maina:
    """ test """
    a=43
    
    def __init__(self):
        self.pio = a
        self.rio = 66
        # print (f"__repr__ {self.__repr__} dict {self.__dict__} self __str__{self.__str__}")
        self.muli()
    
    def muli(self):
        self.mai = 'we'
        print (f"muli{12}")
        return 2

s2 = Maina()
# print (f"s2{s2}")
# print (f"s2.a {s2.a}")

import numpy as np

# my_array = np.array([], 'float64')
my_array = np.array([]) # все равно будет float64
my_array = np.append(my_array, 10)


# print (f"my_arr type {my_array.dtype}")
d= [2,3,2]
d.append(2)
ds = set(d)
# print (f"ds{ds}")

ad = [[23,3],(0,0),[1,3.]]
adn = np.array(ad)
# print (f"adn shape{adn.shape} dtype {adn.dtype}")

a= [0,1,2,3,4]
print (f"{a[2:4]}") # [2,3] последний индекс не включится