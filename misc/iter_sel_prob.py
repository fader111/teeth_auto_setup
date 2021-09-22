a= ["wer3", "dfr3", "nj3u"]
sw = [i for i in a if f"er{3}" in i]
# print (f"sw{sw}")

l1 = [[[],[]],[[],[]],[[],[]]]
# print (f"len {len(l1)}")            # 3
import numpy as np 
ln1 = np.array(l1)
# print (f"ln1 shape {ln1.shape}")    # (3,2,0)
# print (f"ln1 len {len(ln1)}")       # 3

asd = [10e100]
l = 1
if l< min(asd):
    asd.append(l)
    print (f"min {min(asd)} asd {asd}")