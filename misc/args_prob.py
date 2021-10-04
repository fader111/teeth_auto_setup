class A1:
    def a(self, *args, shaw=True):
        for i in range(len(args)):
            print (f"args {args[i]}")
        print(shaw)
        print (f"args len {len(args)} args {args}")
        print (f"self{A1}")
ex = A1().a(45)


def a(*args, shaw=True):
        for i in range(len(args)):
            print (f"args {args[i]}")
        print(shaw)
        print (f"args len {len(args)} args {args}")

a(3,2)

import numpy as np
aa = np.array([[1,2], [1,2],[1,2],[1,2]])
aa[:1][1]

a= np.ones([10])
a *=200
# [a for a in a if a>100 else 300]
a if a>0 else 0
# if 200 in a:
    # print (f"200")
a
# a = np.where((a == 200.), 0, a) робит
# a if a <100 else 0
a= np.array([[1,1.001],[2,3]])
a
a[a<0.1] =0 
a
if 0 in a:
    print('ema')
else:   
    print (f"nema!!")



