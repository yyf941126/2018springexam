import matplotlib.image
import numpy as np
import scipy.misc
import copy
import random
im = matplotlib.image.imread('billgates.jpg')
print(im.shape)
im1=im[:248,:248,:]
[m,n,l]=im1.shape
AA=[]
BB=[]
for i in range(0,8):

    m_start=i*31
    m_end=(i+1)*31

    AA.append(im1[m_start:m_end,:,:])

AA=np.array(AA)
print(AA.shape)

im2=copy.deepcopy(im1)
a=np.zeros(9,dtype=np.int32)
for i in range(0,8):
    a[i]=(i*31)
a[8]=248


RD1=list(range(8))
random.shuffle(RD1)
for i in range(0,8):
    im2[a[i]:a[i+1]]=AA[RD1[i]]

for j in range(0,8):

    n_start=j*31
    n_end=(j+1)*31

    BB.append(im2[:,n_start:n_end,:])


BB=np.array(BB)
print(BB.shape)
RD2=list(range(8))
random.shuffle(RD2)
for i in range(0,8):
    im2[:,a[i]:a[i+1]]=BB[RD2[i]]


scipy.misc.imsave('bill.jpg',im2)



