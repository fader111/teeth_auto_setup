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
