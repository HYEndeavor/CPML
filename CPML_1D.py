#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: V_King
"""
import numpy as np
import pandas as pd
import math
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d
import copy
from PIL import Image, ImageDraw

r, n, d, m = 10**(-6), 377, 20, 4
E0, U0 = 8.85 * 10**(-12), 4 * math.pi * 10**(-7)
dt = (E0 * U0)**(1/2)
t, N, f, L, C, M = dt*100, 100, 3*10**7, 100, 1/(E0 * U0)**(1/2), 100
dx = dy = L / M
sxmax = -(m + 1) * math.log(r) / (2 * n * d * dx)
sx0 = -math.log(r) * math.log(3)/(2 * n * dx * (3**d - 1))
sx = []
sxm = []
data = []
H1 = []
Eynew = []
phx = []
pex = []
aex = []
aey = []
ahx = []
ahy = []
bex = []
bey = []
bhx = []
bhy = []
for i in range(M+1):
    sx.append(0.0)
    sxm.append(0.0)
    H1.append(0.0)
    Eynew.append(0.0)
    phx.append(0.0)
    pex.append(0.0)
    aex.append(0.0)
    aey.append(0.0)
    ahx.append(0.0)
    ahy.append(0.0)
    bex.append(0.0)
    bey.append(0.0)
    bhx.append(0.0)
    bhy.append(0.0)


for i in range(0, 20):  # 电导率进行初始化
    sx[i + 1] = ((20 - i - 0.5) / d)**m * sxmax
    sxm[i] = ((20 - i) / d)**m * sxmax
    sx[M - i] = ((20 - i - 0.5)/d)**m * sxmax
    sxm[M - i] = ((20 - i)/d)**m * sxmax
for i in range(M+1):
    aex[i] = math.e**(-sx[i] * dt/E0) - 1
    bex[i] = aex[i] + 1
    ahx[i] = math.e**(-sxm[i] * dt/E0) - 1
    bhx[i] = ahx[i] + 1
for i in range(1, N):
    H1[50] = math.sin(2 * math.pi * f * i * dt)
    for j in range(1, M):
        pex[j] = bex[j] * pex[j] + aex[j] * (H1[j-1] - H1[j])/dx
        Eynew[j] = Eynew[j] + dt/(dx * E0) * (H1[j-1] - H1[j]) + dt/E0*pex[j]

    for j in range(0, M):
        phx[j] = bhx[j] * phx[j] + ahx[j] * (Eynew[j+1] - Eynew[j])/dx
        H1[j] = H1[j] - dt/(U0 * dx) * (Eynew[j+1] - Eynew[j]) + dt/U0 * (-phx[j])
    data.append(copy.deepcopy(H1))
# 此处可以设置数据的输出方式，如果只想输出某个时刻的图像，去掉循环，将i（小于99）改为具体的值即可
for i in range(0,98,5):
    plt.plot(data[i])
    plt.show()
array_1 = np.array(data)
data = pd.DataFrame(array_1)

writer = pd.ExcelWriter('test.xlsx')
data.to_excel(writer, 'sheet_1', float_format='%.6f')
writer.save()
writer.close()
