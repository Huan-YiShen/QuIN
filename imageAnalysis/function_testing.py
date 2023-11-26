# Implementation of matplotlib function 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm 
from curveFitting import generate_probola

def test_colorbar():  
    dx, dy = 0.015, 0.05
    y, x = np.mgrid[slice(-4, 4 + dy, dy), 
                    slice(-4, 4 + dx, dx)] 
    z = (1 - x / 3. + x ** 5 + y ** 5) * np.exp(-x ** 2 - y ** 2) 
    z = z[:-1, :-1] 
    print(type(z))
    z_min, z_max = -np.abs(z).max(), np.abs(z).max() 
    
    c = plt.imshow(z, cmap ='Greens', vmin = z_min, vmax = z_max, 
                    extent =[x.min(), x.max(), y.min(), y.max()], 
                        interpolation ='nearest', origin ='upper') 
    plt.colorbar(c) 
    
    plt.title('matplotlib.pyplot.imshow() function Example',  
                                        fontweight ="bold") 
    plt.show() 


# digitize that shifts all the value to it's lower basket
def basket(narray2D, bins):
    binedVal = []
    for row in narray2D:
        binedVal.append(np.digitize(row,bins,right=True))
    return binedVal


def test_digitize():
    x = np.array([1.2, 10.0, 12.4, 15.5, 20.])
    bins = np.array([0, 5, 10, 15, 20])
    res = basket(x, bins)
    print(res)


def test_imshow():
    arr = np.array(
        [[1,2,4,8,16],
         [2,4,8,16,32],
         [4,8,16,32,64],
         [8,16,32,64,182],
         [16,32,64,182,256]])
    plt.imshow(arr.T, cmap ='gray', origin='lower') 
    
    x, y = generate_probola(1, xc = 2, yc = 0, x_half_range=2)
    plt.plot(x,y)
    plt.show()

test_imshow()